import framebuf

vol = bytearray(b'\x01\xc1\x00\x02@\x80\x04D@\x08B \xf0Q \x80I\x10\x80D\x90\x80D\x90\x80D\x90\x80I\x10\xf0Q \x08B \x04D@\x02@\x80\x01\xc1\x00\x00\x00\x00')
left_bits = bytearray(b'\x80\xc0\xe0\xf0')
right_bits = bytearray(b'\xf0p0\x10')
left_bits_frame = framebuf.FrameBuffer(left_bits, 4, 4, framebuf.MONO_HLSB)
vol_frame = framebuf.FrameBuffer(vol, 20, 16, framebuf.MONO_HLSB)
right_bits_frame = framebuf.FrameBuffer(right_bits, 4, 4, framebuf.MONO_HLSB)

def image_lbits(x, y):
    return left_bits_frame, x, y

def image_rbits(x,y):
    return right_bits_frame, x, y

def vol(x,y):
    return vol_frame, x, y