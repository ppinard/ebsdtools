package rmlimage.module.ebsd.python.interfaces;

public interface MaskDisc {

    /**
    Return the radius of the disc mask
     */
    public int getradius();

    /**
    Return the x coordinate of the centroid of the circle
     */
    public int getcentroid_x();

    /**
    Return the y coordinate of the centroid of the circle
     */
    public int getcentroid_y();

}
