#!/usr/bin/env python
"""
Script that converts black background and white background images into alpha layer backgrounds.
From: http://www.visitusers.org/index.php?title=Extracting_alpha
"""

def makeAlpha(whiteFile, blackFile):
    from PIL import Image, ImageChops
    W = Image.open(whiteFile)
    Wdata = W.getdata()
    B = Image.open(blackFile)
    Bdata = B.getdata()
    alpha = ImageChops.subtract(W, B)
    alpha = alpha.convert("L")
    alphaData = alpha.getdata()
    out = Image.new("RGBA", W.size)
    outData = list(out.getdata())
    size = W.size
    count = 0
    for y in range(size[1]):
        for x in range(size[0]):
            Bp = B.getpixel((x,y))
            a = alpha.getpixel((x,y))
            r = Bp[0]/255.
            g = Bp[1]/255.
            b = Bp[2]/255.
            a = a / 255.
            a = 1 - a
            if a > 0.0:
                r = r / a
                g = g / a
                b = b / a
            r = int(r*256)
            g = int(g*256)
            b = int(b*256)
            a = int(a*256)
            outData[count] = (r, g, b, a)
            count += 1
    out.putdata(outData)
    return out

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        print >>sys.stderr, "Usage: %s whiteImage blackImage outputImage"%sys.argv[0]
        sys.exit(1)
    whiteFile = sys.argv[1]
    blackFile = sys.argv[2]
    outFile = sys.argv[3]
    makeAlpha(sys.argv[1], sys.argv[2]).save(sys.argv[3])