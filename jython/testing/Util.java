package rmlimage.test;

import java.io.File;
import java.io.IOException;

import org.junit.Assert;

import rmlimage.io.BmpFilter;
import rmlimage.kernel.BinMap;
import rmlimage.kernel.ByteMap;
import rmlimage.kernel.Map;

import rmlshared.io.FileUtil;






public class Util
{

  public static File getFile(String fileName)
  {
    File file = FileUtil.getFile(fileName);
    if (file == null)  Assert.fail(fileName + " not found.");
    
    return file;
  }

  
  
  public static BinMap loadBinMap(String fileName)
  {
    Map map = loadMap(fileName);
    if (!(map instanceof BinMap))  
      Assert.fail(fileName + " is a " + map.getClass().getName() + " not a "
                  + BinMap.class.getName());
                  
    return (BinMap)map;
  }


  
  public static BinMap loadBinMap(File file)
  {
    Map map = loadMap(file);
    if (!(map instanceof BinMap))  
      Assert.fail(file + " is a " + map.getClass().getName() + " not a "
                  + BinMap.class.getName());
                  
    return (BinMap)map;
  }

  
  
  
  public static ByteMap loadByteMap(String fileName)
  {
    Map map = loadMap(fileName);
    if (!(map instanceof ByteMap))  
      Assert.fail(fileName + " is a " + map.getClass().getName() + " not a "
                  + ByteMap.class.getName());
                  
    return (ByteMap)map;
  }
  

  public static ByteMap loadByteMap(File file)
  {
    Map map = loadMap(file);
    if (!(map instanceof ByteMap))  
      Assert.fail(file + " is a " + map.getClass().getName() + " not a "
                  + ByteMap.class.getName());
                  
    return (ByteMap)map;
  }


  
  public static Map loadMap(String fileName)
  {
    return loadMap(getFile(fileName));
  }
  
  

  public static Map loadMap(File file)
  {
    try
      {
        return (Map)new BmpFilter().load(file);
      }
    catch (IOException e)
      {
        Assert.fail(e.getMessage());
        return null;
      }
  }



}
