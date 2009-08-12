package rmlimage.module.ebsd.python.interfaces;


import rmlimage.core.BinMap;


public interface MaskDiscFactory
{

/**
 * Return a <dfn>BinMap</dfn> holding a disc mask.
 *
 * @param   width       width of the <dfn>BinMap</dfn>
 * @param   height      height of the <dfn>BinMap</dfn>
 * @param   centroidX   x coordinate of the center of the disk
 * @param   centroidY   y coordinate of the center of the disk
 * @param   radius      radius of the disk
 */
  public BinMap create(int width, int height, int centroidX, int centroidY, 
                       int radius);
}

