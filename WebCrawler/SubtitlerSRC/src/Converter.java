/*
    This file is part of Google2SRT.

    Google2SRT is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    Google2SRT is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Google2SRT.  If not, see <http://www.gnu.org/licenses/>.
 */

/**
 *
 * @author kom
 * @version "0.6, 08/11/13"
 */

import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.List;
import org.jdom.Document;
import org.jdom.Element;
import org.jdom.JDOMException;
import org.jdom.input.SAXBuilder;

public class Converter {
    private String strOutput;
    private InputStreamReader isrInput;
    private double increment;

    
    public Converter(InputStreamReader isrInput, String strOutput, double increment) {
        this.isrInput = isrInput;
        this.strOutput = strOutput;
        this.increment = increment;
    }
    
    private String tsrt(String duration) { // returns duration in SRT format
        String resultat = "";
        Integer idur, iaux;
        Double dd;
        String saux;
        
        dd = Double.valueOf(duration);
        dd = Double.valueOf(dd.doubleValue() + this.increment);
        
        idur = Integer.valueOf(dd.intValue());
        
        iaux = Integer.valueOf(idur.intValue() / 3600);
        if (iaux < 10)
            resultat += "0";
        resultat += iaux.toString(); // hours
        
        resultat += ":";
        
        iaux = Integer.valueOf((idur.intValue()%3600) / 60);
        if (iaux < 10)
            resultat += "0";
        resultat += iaux.toString(); // mins
        
        resultat += ":";
        
        iaux = Integer.valueOf(idur.intValue()%60);
        if (iaux < 10)
            resultat += "0";
        resultat += iaux.toString(); // seconds
        
        resultat += ",";
        
        dd = Double.valueOf(dd.doubleValue() - dd.intValue());
        
        saux = Double.toString(dd);
        
        switch (saux.length()) {
            case 3: // 0.x
                resultat += saux.substring(2, 3) + "00";
                break;
            case 4: // 0.xx
                resultat += saux.substring(2, 4) + "0";
                break;
            default: // 0.xxx.........
                if (saux.length() >= 5) // case <3 --> ERROR!!
                    resultat += saux.substring(2, 5);
        }
        
        return resultat;
    }
    
    public boolean run() {
        return this.start();
    }
    
    private boolean start() {
        int i, tam;
        SAXBuilder parser = new SAXBuilder();
        Document gSub;
        try {
            gSub = parser.build(isrInput);
        } catch (JDOMException ex) {

            return false;
        } catch (IOException ex) {

            return false;
        }


        Element gSubRoot = gSub.getRootElement();
        List<Element> gSubRootChildren = gSubRoot.getChildren();
        Element child, post;
        String iTime, fTime, duration; // subtitle start / end
        double dFi;
        String text;

        OutputStreamWriter f;

        if (gSubRootChildren.isEmpty()) {

            return false;
        }
        try {
            f = new OutputStreamWriter(new FileOutputStream(strOutput), "UTF-8");
        } catch (IOException ex) {

            return false;
        }
        
        try {
            f.write("\ufeff"); // UTF-8 BOM: EF BB BF
        } catch(IOException ex) {

                return false;
        }
        
        tam = gSubRootChildren.size();
        for (i=0; i<tam; i++) {
            child = gSubRootChildren.get(i);
            iTime = child.getAttributeValue("start"); // start time

            duration = child.getAttributeValue("dur");
            if (duration != null) { // duration is set
                dFi = Double.valueOf(iTime).doubleValue();
                dFi += Double.valueOf(duration).doubleValue();
                fTime = (Double.valueOf(dFi)).toString(); // end time
            } else { // duration is not set
                if (i+1 < tam) { // all but the last element
                    post = gSubRootChildren.get(i+1);
                    fTime = post.getAttributeValue("start"); // start time
                } else { // last element --> +10 seconds
                    dFi = Double.valueOf(iTime).doubleValue();
                    dFi += Double.valueOf(10.0).doubleValue();
                    fTime = (Double.valueOf(dFi)).toString(); // end time
                }
            }


            text = child.getText(); // text
            text = text.replaceAll("&quot;", "\"");
            text = text.replaceAll("&amp;", "&");
            text = text.replaceAll("&#39;", "'");
            text = text.replaceAll("&lt;", "<");
            text = text.replaceAll("&gt;", ">");

            try {
                f.write(String.valueOf(i+1)); f.write("\r\n");
                f.write(tsrt(iTime) + " --> " + tsrt(fTime));
                f.write("\r\n");
                f.write(text); f.write("\r\n");
                f.write("\r\n");
            } catch(IOException ex) {

                return false;
            }
        }
        try {
            f.close();
        } catch(IOException ex) {

            return false;
        }
        return true; // ok!
    }

}
