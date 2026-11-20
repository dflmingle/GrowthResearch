import jadx.api.*;
import java.io.*;
import java.nio.file.*;
import java.util.*;
import java.util.regex.*;
public class SelectJadx {
 public static void main(String[] argv) throws Exception {
  JadxArgs a=new JadxArgs();a.setInputFile(new File(argv[0]));a.setSkipResources(true);a.setThreadsCount(1);
  a.setShowInconsistentCode(true);a.setInlineMethods(false);a.setInlineAnonymousClasses(false);a.setMoveInnerClasses(false);
  Path out=Path.of(argv[1]);Files.createDirectories(out);
  Pattern pattern=Pattern.compile(argv[2]);int max=argv.length>3?Integer.parseInt(argv[3]):200,count=0;
  try(JadxDecompiler d=new JadxDecompiler(a)) {
   d.load();List<String> all=new ArrayList<>();
   for(JavaClass c:d.getClasses()){String n=c.getFullName();all.add(n);}
   Files.write(out.resolve("class-index.txt"),all);
   for(JavaClass c:d.getClasses()){
    String n=c.getFullName();if(!pattern.matcher(n).find())continue;
    try{Path f=out.resolve(n.replace('.','/')+".java");Files.createDirectories(f.getParent());Files.writeString(f,c.getCode());System.out.println("SAVED "+n);count++;}
    catch(Throwable ex){System.out.println("FAILED "+n+" "+ex.getClass().getName());}
    if(count>=max)break;
   }
  }
  System.out.println("DONE "+count);
 }
}
