/*
 * Copyright (c) 2009 Michael Steil, James Abbatiello
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 * OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 * LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 * OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

//#define NO_CLRHOME

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#ifdef _WIN32
#include <direct.h>  // getcwd, chdir
#include <windows.h> // GetLocalTime, SetLocalTime
#else
#include <sys/time.h>
#include <unistd.h>
#endif
#include "stat.h"
#include "readdir.h"
#include "plugin.h"
#include "glue.h"
#include "console.h"

unsigned char RAM[65536];

int
stack4(unsigned short a, unsigned short b, unsigned short c, unsigned short d) {
//	printf("stack4: %x,%x,%x,%x\n", a, b, c, d);
	if (STACK16(S+1) + 1 != a) return 0;
	if (STACK16(S+3) + 1 != b) return 0;
	if (STACK16(S+5) + 1 != c) return 0;
	if (STACK16(S+7) + 1 != d) return 0;
	return 1;
}

/*
 * CHRGET/CHRGOT
 * CBMBASIC implements CHRGET/CHRGOT as self-modifying
 * code in the zero page. This cannot be done with
 * static recompilation, so here is a reimplementation
 * of these functions in C.
0073   E6 7A      INC $7A
0075   D0 02      BNE $0079
0077   E6 7B      INC $7B
0079   AD XX XX   LDA $XXXX
007C   C9 3A      CMP #$3A   ; colon
007E   B0 0A      BCS $008A
0080   C9 20      CMP #$20   ; space
0082   F0 EF      BEQ $0073
0084   38         SEC
0085   E9 30      SBC #$30   ; 0
0087   38         SEC
0088   E9 D0      SBC #$D0
008A   60         RTS
*/
static void
CHRGET_common(int inc) {
	unsigned short temp16;
	if (!inc) goto CHRGOT_start;
CHRGET_start:
	RAM[0x7A]++; SETSZ(RAM[0x7A]);
	if (!Z) goto CHRGOT_start;
	RAM[0x7B]++; SETSZ(RAM[0x7B]);
CHRGOT_start:
	A = RAM[RAM[0x7A] | RAM[0x7B]<<8]; SETSZ(A);
	temp16 = ((unsigned short)A) - ((unsigned short)0x3A); SETNC(temp16); SETSZ(temp16&0xFF);
	if (C) return;
	temp16 = ((unsigned short)A) - ((unsigned short)0x20); SETNC(temp16); SETSZ(temp16&0xFF);
	if (Z) goto CHRGET_start;
	C = 1;
	temp16 = (unsigned short)A-(unsigned short)0x30-(unsigned short)(1-C); SETV(((A ^ temp16) & 0x80) && ((A ^ 0x30) & 0x80)); A = (unsigned char)temp16; SETSZ(A); SETNC(temp16);
	C = 1;
	temp16 = (unsigned short)A-(unsigned short)0xD0-(unsigned short)(1-C); SETV(((A ^ temp16) & 0x80) && ((A ^ 0xD0) & 0x80)); A = (unsigned char)temp16; SETSZ(A); SETNC(temp16);
}

void
CHRGET() {
	CHRGET_common(1);
}
void
CHRGOT() {
	CHRGET_common(0);
}


/************************************************************/
/* KERNAL interface implementation                          */
/* http://members.tripod.com/~Frank_Kontros/kernal/addr.htm */
/************************************************************/

/* KERNAL constants */
#if 0
#define RAM_BOT 0x0400 /* we could just as well start at 0x0400, as there is no screen RAM */
#else
#define RAM_BOT 0x0800
#endif
#define RAM_TOP 0xA000
#define KERN_ERR_NONE			0
#define KERN_ERR_FILE_NOT_FOUND		4
#define KERN_ERR_DEVICE_NOT_PRESENT	5
#define KERN_ERR_MISSING_FILE_NAME	8
#define KERN_ERR_ILLEGAL_DEVICE_NUMBER	9

/* KERNAL internal state */
unsigned char kernal_msgflag, kernal_status = 0;
unsigned short kernal_filename;
unsigned char kernal_filename_len;
unsigned char kernal_lfn, kernal_dev, kernal_sec;
int kernal_quote = 0;

/* shell script hack */
int readycount = 0;
int interactive;
FILE *input_file;

int
init_os(int argc, char **argv) {
//	printf("init_os %d\n", argc);
	if (!argc) /* continuation */
		return PC;

	if (argc>1) {
		interactive = 0;
		input_file = fopen(argv[1], "r");
		if (fgetc(input_file)=='#') {
			char c;
			do {
				c = fgetc(input_file);
			} while((c!=13)&&(c!=10));
		} else {
			fseek(input_file, 0, SEEK_SET);
		}
	} else {
		interactive = 1;
		input_file = NULL;
	}
	srand((unsigned int)time(NULL));

	return 0xE394; /* main entry point of BASIC */
}

unsigned short orig_error, orig_main, orig_crnch, orig_qplop, orig_gone, orig_eval;

int plugin = 0;

void
replace_vector(unsigned short address, unsigned short new, unsigned short *old) {
	*old = RAM[address] | (RAM[address+1]<<8);
	RAM[address] = (new)&0xFF;
	RAM[address+1] = (new)>>8;
}

void
plugin_on() {
	if (plugin)
		return;

	replace_vector(VEC_ERROR, MAGIC_ERROR, &orig_error);
	replace_vector(VEC_MAIN, MAGIC_MAIN, &orig_main);
	replace_vector(VEC_CRNCH, MAGIC_CRNCH, &orig_crnch);
	replace_vector(VEC_QPLOP, MAGIC_QPLOP, &orig_qplop);
	replace_vector(VEC_GONE, MAGIC_GONE, &orig_gone);
	replace_vector(VEC_EVAL, MAGIC_EVAL, &orig_eval);
	
	plugin = 1;
}

static void
plugin_off() {
	unsigned short dummy;

	if (!plugin)
		return;

	replace_vector(VEC_ERROR, orig_error, &dummy);
	replace_vector(VEC_MAIN, orig_main, &dummy);
	replace_vector(VEC_CRNCH, orig_crnch, &dummy);
	replace_vector(VEC_QPLOP, orig_qplop, &dummy);
	replace_vector(VEC_GONE, orig_gone, &dummy);
	replace_vector(VEC_EVAL, orig_eval, &dummy);

	plugin = 0;
}

static void
SETMSG() {
		kernal_msgflag = A;
		A = kernal_status;
}

static void
MEMTOP() {
#if DEBUG /* CBMBASIC doesn't do this */
	if (!C) {
		printf("UNIMPL: set top of RAM");
		exit(1);
	}
#endif
	X = RAM_TOP&0xFF;
	Y = RAM_TOP>>8;

	/*
	 * if we want to turn on the plugin
	 * automatically at start, we can do it here.
	 */
	//plugin_on();
}

/* MEMBOT */
static void
MEMBOT() {
#if DEBUG /* CBMBASIC doesn't do this */
	if (!C) {
		printf("UNIMPL: set bot of RAM");
		exit(1);
	}
#endif
	X = RAM_BOT&0xFF;
	Y = RAM_BOT>>8;
}

/* READST */
static void
READST() {
		A = kernal_status;
}

/* SETLFS */
static void
SETLFS() {
		kernal_lfn = A;
		kernal_dev = X;
		kernal_sec = Y;
}

/* SETNAM */
static void
SETNAM() {
		kernal_filename = X | Y<<8;
		kernal_filename_len = A;
}

/* OPEN */
static void
OPEN() {
		printf("UNIMPL: OPEN\n");
		exit(1);
}

/* CLOSE */
static void
CLOSE() {
		printf("UNIMPL: CLOSE\n");
		exit(1);
}

/* CHKIN */
static void
CHKIN() {
		printf("UNIMPL: CHKIN\n");
		exit(1);
}

/* CHKOUT */
static void
CHKOUT() {
		printf("UNIMPL: CHKOUT\n");
		exit(1);
}

/* CLRCHN */
static void
CLRCHN() {
#ifdef DEBUG
		printf("WARNING: UNIMPL: CLRCHN\n");
#endif
}

static const char run[] = { 'R', 'U', 'N', 13 };

int fakerun = 0;
int fakerun_index = 0;

/* CHRIN */
static void
CHRIN() {
	if ((!interactive) && (readycount==2)) {
		exit(0);
	}
	if (!input_file) {
		A = getchar(); /* stdin */
	} else {
		if (fakerun) {
			A = run[fakerun_index++];
			if (fakerun_index==sizeof(run))
				input_file = 0; /* switch to stdin */
		} else {
			A = fgetc(input_file);
			if ((A==255)&&(readycount==1)) {
				fakerun = 1;
				fakerun_index = 0;
				A = run[fakerun_index++];
			}
		}
	}
	if (A==255)
		exit(0);
	if (A=='\n') A = '\r';
	C = 0;
}

/* CHROUT */
static void
CHROUT() {
#if 0
int a = *(unsigned short*)(&RAM[0x0100+S+1]) + 1;
int b = *(unsigned short*)(&RAM[0x0100+S+3]) + 1;
int c = *(unsigned short*)(&RAM[0x0100+S+5]) + 1;
int d = *(unsigned short*)(&RAM[0x0100+S+7]) + 1;
printf("CHROUT: %d @ %x,%x,%x,%x\n", A, a, b, c, d);
#endif
	if (!interactive) {
		if (stack4(0xe10f,0xab4a,0xab30,0xe430)) {
			/* COMMODORE 64 BASIC V2 */
			C = 0;
			return;
		}
		if (stack4(0xe10f,0xab4a,0xab30,0xe43d)) {
			/* 38911 */
			C = 0;
			return;
		}
		if (stack4(0xe10f,0xab4a,0xab30,0xe444)) {
			/* BASIC BYTES FREE */
			C = 0;
			return;
		}
	}
	if (stack4(0xe10f,0xab4a,0xab30,0xa47b)) {
		/* READY */
		if (A=='R') readycount++;
		if (!interactive) {
			C = 0;
			return;
		}
	}
	if (stack4(0xe10f,0xab4a,0xaadc,0xa486)) {
		/*
		 * CR after each entered numbered program line:
		 * The CBM screen editor returns CR when the user
		 * hits return, but does not print the character,
		 * therefore CBMBASIC does. On UNIX, the terminal
		 * prints all input characters, so we have to avoid
		 * printing it again
		 */
		C = 0;
		return;
	}
	
#if 0
	printf("CHROUT: %c (%d)\n", A, A);
#else
	switch (A) {
		case 10:
			kernal_quote = 0;
			break;
		case 13:
			kernal_quote = 0;
			putchar(13);
			putchar(10);
			break;
		case 17: /* CSR DOWN */
			down_cursor();
			break;
		case 19: /* CSR HOME */
			move_cursor(0, 0);
			break;
		case 29: /* CSR RIGHT */
			right_cursor();
			break;
		case 145: /* CSR UP */
			up_cursor();
			break;
		case 147: /* clear screen */
#ifndef NO_CLRHOME
			if (!kernal_quote)
				clear_screen();
#endif
			break;
		case 157: /* CSR LEFT */
			left_cursor();
			break;
		case '"':
			kernal_quote = 1-kernal_quote;
			// fallthrough
		default:
			putchar(A);
	}
#endif
	fflush(stdout);
	C = 0;
}

/* LOAD */
static void
LOAD() {
		FILE *f;
		struct stat st;
		unsigned short start;
		unsigned short end;
		unsigned char savedbyte;

		if (A) {
			printf("UNIMPL: VERIFY\n");
			exit(1);
		}
		if (!kernal_filename_len)
			goto missing_file_name;

/* on special filename $ read directory entries and load they in the basic area memory */
		if( RAM[kernal_filename]=='$' ) {
			DIR *dirp;
			struct dirent *dp;
			int i, file_size;
			unsigned short old_memp, memp = 0x0801;  // TODO hack!

			old_memp = memp;
			memp += 2;
			RAM[memp++] = 0;
			RAM[memp++] = 0;
			RAM[memp++] = 0x12; /* REVERS ON */
			RAM[memp++] = '"';
			for(i=0; i<16; i++)
				RAM[memp+i] = ' ';
			if( (getcwd((char*)&RAM[memp], 256)) == NULL )
				goto device_not_present;
			memp += strlen((char*)&RAM[memp]); /* only 16 on COMMODORE DOS */
			RAM[memp++] = '"';
			RAM[memp++] = ' ';
			RAM[memp++] = '0';
			RAM[memp++] = '0';
			RAM[memp++] = ' ';
			RAM[memp++] = '2';
			RAM[memp++] = 'A';
			RAM[memp++] = 0;

			RAM[old_memp] = (memp) & 0xFF;
			RAM[old_memp+1] = (memp) >> 8;
			
			if ( !(dirp = opendir(".")) )
				goto device_not_present;
			while ((dp = readdir(dirp))) {
				size_t namlen = strlen(dp->d_name);
				stat(dp->d_name, &st);
				file_size = (st.st_size + 253)/254; /* convert file size from num of bytes to num of blocks(254 bytes) */
				if (file_size>0xFFFF)
					file_size = 0xFFFF;
				old_memp = memp;
				memp += 2;
				RAM[memp++] = file_size & 0xFF;
				RAM[memp++] = file_size >> 8;
				if (file_size<1000) {
					RAM[memp++] = ' ';
					if (file_size<100) {
						RAM[memp++] = ' ';
						if (file_size<10) {
							RAM[memp++] = ' ';
						}
					}
				}
				RAM[memp++] = '"';
				if (namlen>16)
					namlen=16; /* TODO hack */
				memcpy(&RAM[memp], dp->d_name, namlen);
				memp += namlen;
				RAM[memp++] = '"';
				for (i=namlen; i<16; i++)
					RAM[memp++] = ' ';
				RAM[memp++] = ' ';
				RAM[memp++] = 'P';
				RAM[memp++] = 'R';
				RAM[memp++] = 'G';
				RAM[memp++] = ' ';
				RAM[memp++] = ' ';
				RAM[memp++] = 0;

				RAM[old_memp] = (memp) & 0xFF;
				RAM[old_memp+1] = (memp) >> 8;
			}
			RAM[memp] = 0;
			RAM[memp+1] = 0;
			(void)closedir(dirp);
			end = memp + 2;
/*
for (i=0; i<255; i++) {
	if (!(i&15))
		printf("\n %04X  ", 0x0800+i);
	printf("%02X ", RAM[0x0800+i]);
}
*/
			goto load_noerr;
		} /* end if( RAM[kernal_filename]=='$' ) */

		savedbyte = RAM[kernal_filename+kernal_filename_len]; /* TODO possible overflow */
		RAM[kernal_filename+kernal_filename_len] = 0;

/* on directory filename chdir on it */
		if( (stat((char*)&RAM[kernal_filename], &st)) == -1 )
			goto file_not_found;
		if(S_ISDIR(st.st_mode)) {
			if( (chdir((char*)&RAM[kernal_filename])) == -1 )
				goto device_not_present;

			RAM[0x0801] = RAM[0x0802] = 0;
			end = 0x0803;
			goto load_noerr;
		}

/* on file load it read it and load in the basic area memory */
		f = fopen((char*)&RAM[kernal_filename], "rb");
		if (!f)
			goto file_not_found;
		start = ((unsigned char)fgetc(f)) | ((unsigned char)fgetc(f))<<8;
		if (!kernal_sec)
			start = X | Y<<8;
		end = start + fread(&RAM[start], 1, 65536-start, f); /* TODO may overwrite ROM */
		printf("LOADING FROM $%04X to $%04X\n", start, end);
		fclose(f);

load_noerr:
		X = end & 0xFF;
		Y = end >> 8;
		C = 0;
		A = kernal_status = KERN_ERR_NONE;
		return;
file_not_found:
		C = 1;
		A = kernal_status = KERN_ERR_FILE_NOT_FOUND;
		return;
device_not_present:
		C = 1;
		A = kernal_status = KERN_ERR_DEVICE_NOT_PRESENT;
		return;
missing_file_name:
		C = 1;
		A = kernal_status = KERN_ERR_MISSING_FILE_NAME;
		return;
}

/* SAVE */
static void
SAVE() {
		FILE *f;
		unsigned char savedbyte;
		unsigned short start;
		unsigned short end;

		start = RAM[A] | RAM[A+1]<<8;
		end = X | Y << 8;
		if (end<start) {
			C = 1;
			A = kernal_status = KERN_ERR_NONE;
			return;
		}
		if (!kernal_filename_len) {
			C = 1;
			A = kernal_status = KERN_ERR_MISSING_FILE_NAME;
			return;
		}
		savedbyte = RAM[kernal_filename+kernal_filename_len]; /* TODO possible overflow */
		RAM[kernal_filename+kernal_filename_len] = 0;
		f = fopen((char*)&RAM[kernal_filename], "wb"); /* overwrite - these are not the COMMODORE DOS semantics! */
		if (!f) {
			C = 1;
			A = kernal_status = KERN_ERR_FILE_NOT_FOUND;
			return;
		}
		fputc(start & 0xFF, f);
		fputc(start >> 8, f);
		fwrite(&RAM[start], end-start, 1, f);
		fclose(f);
		C = 0;
		A = kernal_status = KERN_ERR_NONE;
}

/* SETTIM */
static void
SETTIM() {
    unsigned long   jiffies = Y*65536 + X*256 + A;
    unsigned long   seconds = jiffies/60;
#ifdef _WIN32
	SYSTEMTIME st;

	GetLocalTime(&st);
	st.wHour         = (WORD)(seconds/3600);
	st.wMinute       = (WORD)(seconds/60);
	st.wSecond       = (WORD)(seconds%60);
	st.wMilliseconds = (WORD)((jiffies % 60) * 1000 / 60);
	SetLocalTime(&st);
#else
    time_t  now = time(0);
    struct tm       bd;
    struct timeval  tv;
    
    localtime_r(&now, &bd);

    bd.tm_sec       = seconds%60;
    bd.tm_min       = seconds/60;
    bd.tm_hour      = seconds/3600;

    tv.tv_sec   = mktime(&bd);
    tv.tv_usec  = (jiffies % 60) * (1000000/60);
    
    settimeofday(&tv, 0);
#endif
}

/* RDTIM */
static void
RDTIM() {
	unsigned long   jiffies;
#ifdef _WIN32
	SYSTEMTIME st;

	GetLocalTime(&st);
	jiffies = ((st.wHour*60 + st.wMinute)*60 + st.wSecond)*60 + st.wMilliseconds * 60 / 1000;
#else
    time_t  now = time(0);
    struct tm       bd;
    struct timeval  tv;
    
    localtime_r(&now, &bd);
    gettimeofday(&tv, 0);
    
    jiffies = ((bd.tm_hour*60 + bd.tm_min)*60 + bd.tm_sec)*60 + tv.tv_usec / (1000000/60);
#endif
    Y   = (unsigned char)(jiffies/65536);
    X   = (unsigned char)((jiffies%65536)/256);
    A   = (unsigned char)(jiffies%256);
    
}

/* STOP */
static void
STOP() {
		SETZ(0); /* TODO we don't support the STOP key */
}

/* GETIN */
static void
GETIN() {
	CHRIN();
}

/* CLALL */
static void
CLALL() {
}

/* PLOT */
static void
PLOT() {
		/*
		 * TODO we always return 0/0 as the cursor position
		 * setting the cursor is unused by CBMBASIC
		 */
		X = 0;
		Y = 0;
}


/* IOBASE */
static void
IOBASE() {
#define CIA 0xDC00 /* we could put this anywhere... */
		/*
		 * IOBASE is just used inside RND to get a timer value.
		 * So, let's fake this here, too.
		 * Commodore BASIC reads offsets 4/5 and 6/7 to get the
		 * two timers of the CIA.
		 */
		int pseudo_timer;
		pseudo_timer = rand();
		RAM[CIA+4] = pseudo_timer&0xff;
		RAM[CIA+5] = pseudo_timer>>8;
		pseudo_timer = rand(); /* more entropy! */
		RAM[CIA+8] = pseudo_timer&0xff;
		RAM[CIA+9] = pseudo_timer>>8;
		X = CIA & 0xFF;
		Y = CIA >> 8;
}

int
kernal_dispatch() {
//{ printf("kernal_dispatch $%04X; ", PC); int i; printf("stack (%02X): ", S); for (i=S+1; i<0x100; i++) { printf("%02X ", RAM[0x0100+i]); } printf("\n"); }

	unsigned int new_pc;
	switch(PC) {
		case 0x0073:	CHRGET();	break;
		case 0x0079:	CHRGOT();	break;
		case 0xFF90:	SETMSG();	break;
		case 0xFF99:	MEMTOP();	break;
		case 0xFF9C:	MEMBOT();	break;
		case 0xFFB7:	READST();	break;
		case 0xFFBA:	SETLFS();	break;
		case 0xFFBD:	SETNAM();	break;
		case 0xFFC0:	OPEN();		break;
		case 0xFFC3:	CLOSE();	break;
		case 0xFFC6:	CHKIN();	break;
		case 0xFFC9:	CHKOUT();	break;
		case 0xFFCC:	CLRCHN();	break;
		case 0xFFCF:	CHRIN();	break;
		case 0xFFD2:	CHROUT();	break;
		case 0xFFD5:	LOAD();		break;
		case 0xFFD8:	SAVE();		break;
		case 0xFFDB:	SETTIM();	break;
		case 0xFFDE:	RDTIM();	break;
		case 0xFFE1:	STOP();		break;
		case 0xFFE4:	GETIN();	break;
		case 0xFFE7:	CLALL();	break;
		case 0xFFF0:	PLOT();		break;
		case 0xFFF3:	IOBASE();	break;

		case 0:		plugin_off(); S+=2; break;
		case 1:		plugin_on(); S+=2; break;

		case MAGIC_ERROR:	new_pc = plugin_error(); PUSH_WORD(new_pc? new_pc-1:orig_error-1); break;
		case MAGIC_MAIN:	new_pc = plugin_main(); PUSH_WORD(new_pc? new_pc-1:orig_main-1); break;
		case MAGIC_CRNCH:	new_pc = plugin_crnch(); PUSH_WORD(new_pc? new_pc-1:orig_crnch-1); break;
		case MAGIC_QPLOP:	new_pc = plugin_qplop(); PUSH_WORD(new_pc? new_pc-1:orig_qplop-1); break;
		case MAGIC_GONE:	new_pc = plugin_gone(); PUSH_WORD(new_pc? new_pc-1:orig_gone-1); break;
		case MAGIC_EVAL:	new_pc = plugin_eval(); PUSH_WORD(new_pc? new_pc-1:orig_eval-1); break;
		
		case MAGIC_CONTINUATION: /*printf("--CONTINUATION--\n");*/ return 0;

		default: printf("unknown PC=$%04X S=$%02X\n", PC, S); exit(1);
	}
	return 1;
}

