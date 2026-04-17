SECTIONS
{
    .text.boot: { *(.text.boot) }
    .text: { *(.text) }
    .rodata: { *(.rodata) }
    .data: { *(.data)}
    . = ALIGN(0x8);
    bss_begin = .;
    .bss : { 8(.bss*) }
    bss_end = .;
}