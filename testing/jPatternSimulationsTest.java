package rmlimage.plugin.ebsd.python;


import org.junit.Test;

import rmlimage.kernel.ByteMap;
import rmlimage.plugin.ebsd.python.jPatternSimulations;
import rmlimage.test.Util;



public class jPatternSimulationsTest
{ 
  @Test
  public void patternFCC()
  {  
    jPatternSimulations patt = new jPatternSimulations(335, 255, false, 0.0, 
                                                       0.0, 0.3, 20000.0, 32, 
                                                       70.0);
    ByteMap sim = patt.patternFCC(0.0, 0.0, 0.0);

    ByteMap expected = Util.loadByteMap(
                        "rmlimage/plugin/ebsd/python/jPatternSimulations.bmp");
    sim.assertEquals(expected);
  }
}

