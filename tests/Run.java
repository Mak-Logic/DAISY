import java.io.*; import java.util.*; import java.text.SimpleDateFormat;
import org.javarosa.core.model.*; import org.javarosa.core.model.instance.*;
import org.javarosa.core.model.data.*; import org.javarosa.core.model.data.helper.Selection;
import org.javarosa.core.model.condition.EvaluationContext;
import org.javarosa.model.xform.XPathReference; import org.javarosa.xform.util.XFormUtils;
public class Run {
  public static void main(String[] a) throws Exception {
    String form=a[0]; BufferedReader br=new BufferedReader(new InputStreamReader(new FileInputStream(a[1]),"UTF-8"));
    List<String> outs=new ArrayList<>(); String line; FormDef fd=null; String cid=null;
    PrintStream out=new PrintStream(System.out,true,"UTF-8");
    while((line=br.readLine())!=null){
      line=line.trim(); if(line.isEmpty())continue;
      if(line.startsWith("CASE ")){cid=line.substring(5); fd=XFormUtils.getFormFromInputStream(new FileInputStream(form)); fd.initialize(true,new InstanceInitializationFactory()); outs.clear(); continue;}
      if(line.startsWith("OUT ")){outs.add(line.substring(4)); continue;}
      if(line.equals("END")){
        StringBuilder sb=new StringBuilder("RESULT "+cid);
        for(String p:outs){TreeElement e=el(fd,p); String v=e.getValue()==null?"":e.getValue().getDisplayText(); sb.append("\t"+p.substring(p.lastIndexOf('/')+1)+"="+v+"|rel="+e.isRelevant());}
        out.println(sb); continue;}
      // SET path|type|value
      String[] f=line.substring(4).split("\\|",3); TreeElement e=el(fd,f[0]);
      if(!e.isRelevant()){ out.println("WARN "+cid+" skipped (not shown): "+f[0]+"="+f[2]); continue; }
      IAnswerData d; String t=f[1], v=f[2];
      switch(t){
        case "int": d=new IntegerData(Integer.parseInt(v)); break;
        case "decimal": d=new DecimalData(Double.parseDouble(v)); break;
        case "date": d=new DateData(new SimpleDateFormat("yyyy-MM-dd").parse(v)); break;
        case "select1": d=new SelectOneData(new Selection(v)); break;
        case "select": {Vector<Selection> s=new Vector<>(); for(String x:v.split(" ")) s.add(new Selection(x)); d=new SelectMultiData(s); break;}
        default: d=new StringData(v);
      }
      fd.setValue(d,e.getRef(),true);
    }
  }
  static TreeElement el(FormDef fd,String p){ TreeReference r=XPathReference.getPathExpr(p).getReference(); TreeElement e=fd.getMainInstance().resolveReference(r); if(e==null) throw new RuntimeException("no node "+p); return e;}
}
