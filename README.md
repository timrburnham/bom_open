# bom_open
open() alternative which respects Unicode BOM

Open a file. If reading in text mode and BOM is present, switch to specified Unicode encoding.
Unlike normal open(), always write BOM, even for utf-8 mode.
