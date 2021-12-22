.nds

.open "data/repack/arm9.bin",0x02000000
  .org 0x0208821c
  .area 0xc0
    FONT_DATA:
    .import "data/font_data.bin",0,0x5f
    .align

    GET_CHAR_WIDTH:
    ;Check if the character is ASCII
    cmp r14,0x0
    addlt r2,r2,6
    blt GET_CHAR_WIDTH_RETURN
    cmp r14,0x7f
    addgt r2,r2,6
    bgt GET_CHAR_WIDTH_RETURN
    ;Add to r2 the width of the character in r14
    push {r0}
    ldr r0,=FONT_DATA
    add r0,r0,r14
    sub r0,r0,0x20
    ldrb r0,[r0]
    add r2,r2,r0
    pop {r0}
    b GET_CHAR_WIDTH_RETURN

    ;Divide the max line width by 6
    ;((A * 0xaaab) >> 16) >> 2
    SET_LINE_WIDTH:
    ldr r0,[r4]
    ldr r1,=0xaaab
    mul r0,r0,r1
    lsr r0,r0,16
    lsr r0,r0,2
    str r0,[r4]
    mov r0,0x1
    b SET_LINE_WIDTH_RETURN
    .pool
  .endarea

  .org 0x02021568
    ;add r2,r2,0x1
    b GET_CHAR_WIDTH
    GET_CHAR_WIDTH_RETURN:

  .org 0x0202157c
    ;mov r0,0x1
    b SET_LINE_WIDTH
    SET_LINE_WIDTH_RETURN:

  .include "data/centering.asm"

  ;Redirect all error codes to the first one: WH_SYSSTATE_STOP
  REPLACEMENT equ 0x02087b58

  .org 0x0208811c
  .area 0xec
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
  .endarea

  ; Redirect some more strings
  .org 0x0201d4ac
  .area 0x10
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
  .endarea

  .org 0x0201d668
    .dw REPLACEMENT
    .skip 4
    .dw REPLACEMENT

  .org 0x0201d708
    .dw REPLACEMENT

  .org 0x0201d788
    .dw REPLACEMENT

  .org 0x0201db4c
    .dw REPLACEMENT
    .skip 4
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT

  .org 0x0201dc40
    .dw REPLACEMENT

  .org 0x0201dcf8
    .dw REPLACEMENT

  .org 0x0201dd90
    .dw REPLACEMENT

  .org 0x0201def4
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT

  .org 0x0201e0a4
    .dw REPLACEMENT
    .skip 4
    .dw REPLACEMENT
    .dw REPLACEMENT

  .org 0x0201e508
    .dw REPLACEMENT

  .org 0x0201e588
    .dw REPLACEMENT

  .org 0x0201e870
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT

  .org 0x0201e96c
    .dw REPLACEMENT
    .dw REPLACEMENT
    .skip 4
    .dw REPLACEMENT

  .org 0x0201ea14
    .dw REPLACEMENT

  .org 0x0201eb20
    .dw REPLACEMENT
    .dw REPLACEMENT

  .org 0x0201db54
  .area 0x10
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
  .endarea

  .org 0x0201dc40
    .dw REPLACEMENT

  .org 0x0201dcf8
    .dw REPLACEMENT

  .org 0x0201dd90
    .dw REPLACEMENT

  .org 0x0201def4
  .area 0xc
    .dw REPLACEMENT
    .dw REPLACEMENT
    .dw REPLACEMENT
  .endarea

  .org 0x0208692c
    .dw REPLACEMENT
    .skip 8
    .dw REPLACEMENT
    .skip 8
    .dw REPLACEMENT
    .skip 8
    .dw REPLACEMENT
    .skip 8
    .dw REPLACEMENT
    .skip 8
    .dw REPLACEMENT
    .skip 8
    .dw REPLACEMENT
    .skip 8
    .dw REPLACEMENT
    .skip 8
    .dw REPLACEMENT
    .skip 8
    .dw REPLACEMENT
.close
