#!/usr/bin/env python
import os
from math import ceil

from PIL import (Image as PILImage, ImageDraw)

import settings
import strategies


class ManipulationStrategy(object):
    def manip(self, *args, **kwargs):
        raise NotImplemented


class ManipBlend(ManipulationStrategy):
    def manip(self, img1, img2, filename):
        img1 = PILImage.open(img1.fullpath)
        img2 = PILImage.open(img2.fullpath)
        blended_image = PILImage.blend(img1, img2, 0.5)
        blended_image.save(os.path.join(settings.IMAGE_DIR, filename))
        return blended_image


class ManipCompose(ManipulationStrategy):
    def four_column_mask(self):
        mask = PILImage.new("RGBA", (300,300), "#000000")
        draw = ImageDraw.Draw(mask)
        alpha = 255
        delta = alpha/3.0
        column = 0
        for i in xrange(300):
            if column > 75:
                alpha = alpha - delta
                column = 0
            draw.line((i,0,i,300), fill=(0,0,0,int(ceil(alpha))))
            column += 1
        return mask

    def manip(self, img1, img2, filename):
        mask = self.four_column_mask()
        img1 = PILImage.open(img1.fullpath)
        img2 = PILImage.open(img2.fullpath)
        composed_image = PILImage.composite(img1, img2, mask)
        composed_image.save(os.path.join(settings.IMAGE_DIR, filename))
        return composed_image
