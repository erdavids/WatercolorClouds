import cairo, sys, argparse, copy
import math, random
import PIL
from PIL import Image, ImageDraw

float_gen = x = lambda a, b: random.uniform(a, b)

#shape = [(30,30), (60, 15), (90,90), (200, 120), (150, 200), (30, 30)]

initial = 120
deviation = 50

colors = []
for i in range(15):
    colors.append((float_gen(.4, .75), float_gen(.4, .75), float_gen(.4, .75)))

def octagon(x_orig, y_orig, side):
    x = x_orig
    y = y_orig
    d = side / math.sqrt(2)
    oct = []

    oct.append((x, y))
    
    x += side
    oct.append((x, y))
    
    x += d
    y += d
    oct.append((x, y))

    y += side
    oct.append((x, y))

    x -= d
    y += d
    oct.append((x, y))

    x -= side
    oct.append((x, y))

    x -= d
    y -= d
    oct.append((x, y))

    y -= side
    oct.append((x, y))

    x += d
    y -= d
    oct.append((x, y))

    return oct

def deform(shape, iterations, variance):
    for i in range(iterations):
        for j in range(len(shape)-1, 0, -1):
            midpoint = ((shape[j-1][0] + shape[j][0])/2 + float_gen(-variance, variance), (shape[j-1][1] + shape[j][1])/2 + float_gen(-variance, variance))
            
            shape.insert(j, midpoint)

    return shape

def main():
    width = 3000
    height = 2000
    
    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)
    
    cr.set_source_rgb(.9, .9, .9)
    cr.rectangle(0,0,width,height)
    cr.fill()
    
    cr.set_line_width(1)
    
    for p in range(-int(height*.2), int(height*1.2), 40):
        print p
        cr.set_source_rgba(random.choice(colors)[0], random.choice(colors)[1], random.choice(colors)[2], .02)
        shape = octagon(random.randint(-100, width + 100), p, random.randint(100, 300))
        baseshape = deform(shape, 1, initial)
        for j in range(random.randint(20, 25)):
            tempshape = copy.deepcopy(baseshape)
            layer = deform(tempshape, 1, deviation)
            for i in range(len(layer)):
                cr.line_to(layer[i][0], layer[i][1])
            cr.fill()
#    cr.set_source_rgba(float_gen(0,1), float_gen(0,1), float_gen(0,1), .01)
#    for k in range(200):
#        for i in range(len(shape)):
#            cr.line_to(shape[i][0] + 200 + float_gen(-200, 200), shape[i][1] + 200 + float_gen(-200, 200))
#        cr.fill()


    ims.write_to_png('watercolor.png')

#    pil_image = Image.open('watercolor.png')
#    pixels = pil_image.load()
#
#    for i in range(pil_image.size[0]):
#        for j in range(pil_image.size[1]):
#            r, g, b = pixels[i, j]
#            noise = float_gen(1.0-.4, 1.0+.4)
#            pixels[i, j] = (int(r*noise), int(g*noise), int(b*noise))
#    pil_image.save('textured_watercolor.png')

if __name__ == "__main__":
    main()
