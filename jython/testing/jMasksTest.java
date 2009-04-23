package rmlimage.plugin.ebsd.python;


import org.junit.Test;

import rmlimage.kernel.BinMap;
import rmlimage.plugin.ebsd.python.jMasks;
import rmlimage.test.Util;



public class jMasksTest
{ 
  @Test
  public void discMask()
  {  
    BinMap sim = new jMasks().discMask(168, 128, 84, 64, 64);

    BinMap expected = Util.loadBinMap(
                        "rmlimage/plugin/ebsd/python/jMasks.bmp");
    sim.assertEquals(expected);
  }
}

