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

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.util.HashMap;

public class NetSubtitle {
    public static enum Method {
        Google,                     // [Obsolete] Former Google Video
        YouTubeLegacy,              // YouTube (legacy method). Used by default until v0.5.6. Kept as secondary method in case "new signature method" suddenly stops working.
        YouTubeSignature            // YouTube (new signature method). New method. Required for ASR. Used by default in v0.6
    };
    
    public static enum Tipus {
        GoogleTrack,                // [Obsolete] Former Google Video track
        YouTubeTrack,               // YouTube track
        YouTubeASRTrack,            // YouTube ASR track
        YouTubeTarget               // YouTube target
    };
    
    private Tipus type;
    private String name = "",           // track name
            lang = "",                  // language code
            langOriginal = "",          // language name (untranslated)
            langTranslated = "",        // language name (translated)
            id = null;                  // "docid" (Google Video) o "v" (YouTube)
    private int idXML = -1;             // attribute "id" in XML subs list
    private boolean isDefault;          // attribute "default" in XML subs list
    private boolean isTrack = false;    // is Track or Target?
    
    
    public NetSubtitle() {
        this.isDefault = false; // All but one are "default"
    }
    
    public void setType(Tipus type) {
        this.type = type;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public void setLang(String lang) {
        this.lang = lang;
    }
    
    public void setId(String id) {
        this.id = id;
    }
    
    public void setLangTranslated(String langTrans) {
        this.langTranslated = langTrans;
    }
    
    public void setDefault() {
        this.isDefault = true;
    }

    public void setTrack(boolean isTrack) {
        this.isTrack = isTrack;
    }
    
    public void setIdXML(int id) {
        this.idXML = id;
    }
    
    public void setLangOriginal(String lang) {
        this.langOriginal = lang;
    }
    
     public Tipus getType() {
        return this.type;
    }
    
    public String getName() {
        return this.name;
    }
    
    public String getLang() {
        return this.lang;
    }
    
    public String getId() {
        return this.id;
    }
    
    public boolean isDefault() {
        return this.isDefault;
    }
    
    public boolean isTrack() {
        return this.isTrack;
    }
    
    public String getLangOriginal() {
        return this.langOriginal;
    }
    
    public String getLangTranslated() {
        return this.langTranslated;
    }

    public int getIdXML() {
        return this.idXML;
    }
    
    @Override
    public String toString()
    {
        String s;
        if (this.name.isEmpty())
        {
            switch(this.type)
            {
                case YouTubeASRTrack:
                    s = this.langOriginal + " (" + this.lang + ", [ASR])";
                    break;
                case YouTubeTarget:
                    s = this.langOriginal + " (" + this.lang + ", [TARGET])";
                    break;                    
                default:
                    s = this.langOriginal + " (" + this.lang + ")";
            }
        }
        else
            s = this.langOriginal + " (" + this.lang + ", " + this.name + ")";
        return s;
    }
    
    public String getTrackURL() throws UnsupportedEncodingException
    {
        String s;
        if (Tipus.GoogleTrack.equals(this.type))
            return getTrackURL(Method.Google);
        else
        {
            try
            {
                //Network.setMethod(Method.YouTubeSignature);
                s = getTrackURL(Network.getMethod());
                return s;
            }
            catch (Exception e) {
                Network.setMethod(Method.YouTubeLegacy);
                s = getTrackURL(Network.getMethod());                
                return s;
            }
        }
    }
    
    
    public String getTrackURL(Method method) throws UnsupportedEncodingException {
        String s;
        HashMap<String,String> params;
        
        switch (method) {
            case Google:
                s = "http://video.google.com/videotranscript?frame=c&type=track&" +
                        "name=" + URLEncoder.encode(this.name, "UTF-8") +
                        "&lang=" + URLEncoder.encode(this.lang, "UTF-8") +
                        "&docid=" + URLEncoder.encode(this.id, "UTF-8");
                System.out.println("(DEBUG) Track URL: " + s);
                return s;
            case YouTubeLegacy:
                s = "http://video.google.com/timedtext?type=track&" +
                        "name=" + URLEncoder.encode(this.name, "UTF-8") +
                        "&lang=" + URLEncoder.encode(this.lang, "UTF-8") +
                        "&v=" + URLEncoder.encode(this.id, "UTF-8");
                System.out.println("(DEBUG) Track URL (Legacy): " + s);
                return s;
            case YouTubeSignature:        
                params = Network.getParams();
                s = "https://www.youtube.com/api/timedtext" +
                       "?key=" + params.get("key") +
                       "&expire=" + params.get("expire") +
                       "&sparams=" + params.get("sparams") +
                       "&signature=" + params.get("signature") +
                       "&caps=" + params.get("caps") +
                       "&asr_langs=" + params.get("asr_langs") +
                        
                       "&name=" + URLEncoder.encode(this.name, "UTF-8") +
                       "&lang=" + URLEncoder.encode(this.lang, "UTF-8") +
                       "&v=" + URLEncoder.encode(this.id, "UTF-8") +
                        
                       "&type=track";
                
                if (NetSubtitle.Tipus.YouTubeASRTrack.equals(this.type))
                {
                    s += "&kind=asr";
                    System.out.println("(DEBUG) Track ASR URL (Signature): " + s);
                }
                else
                {
                    System.out.println("(DEBUG) Track URL (Signature): " + s);
                }
                
                return s;                
        }
        return null;
    }
    
    public String getTargetURL(NetSubtitle source) throws UnsupportedEncodingException {
        String s;
        try
        {
            //Network.setMethod(Method.YouTubeSignature);
            s = getTargetURL(Network.getMethod(), source);
            return s;
        }
        catch (Exception e) {
            Network.setMethod(Method.YouTubeLegacy);
            s = getTargetURL(Network.getMethod(), source);
            return s;
        }
    }
    
    public String getTargetURL(Method method, NetSubtitle source) throws UnsupportedEncodingException {
        String s;
        HashMap<String,String> params;
        
        switch (method) {
            // Other cases are unsupported
            case YouTubeLegacy:
                s = "http://video.google.com/timedtext?type=track&" +
                        "name=" + URLEncoder.encode(source.name, "UTF-8") +
                        "&lang=" + URLEncoder.encode(source.lang, "UTF-8") +
                        "&tlang=" + URLEncoder.encode(this.lang, "UTF-8") +
                        "&v=" + URLEncoder.encode(source.id, "UTF-8");
                System.out.println("(DEBUG) Target URL (Legacy): " + s);
                return s;
            case YouTubeSignature:                
                params = Network.getParams();
                s = "https://www.youtube.com/api/timedtext" +
                       "?key=" + params.get("key") +
                       "&expire=" + params.get("expire") +
                       "&sparams=" + params.get("sparams") +
                       "&signature=" + params.get("signature") +
                       "&caps=" + params.get("caps") +
                       "&asr_langs=" + params.get("asr_langs") +
                        
                       "&name=" + URLEncoder.encode(source.name, "UTF-8") +
                       "&lang=" + URLEncoder.encode(source.lang, "UTF-8") +
                       "&tlang=" + URLEncoder.encode(this.lang, "UTF-8") +
                       "&v=" + URLEncoder.encode(source.id, "UTF-8") +
                
                       "&type=track";
                
                if (NetSubtitle.Tipus.YouTubeASRTrack.equals(source.type))
                {
                    s += "&kind=asr";
                    System.out.println("(DEBUG) Target ASR URL (Signature): " + s);
                }
                else
                {
                    System.out.println("(DEBUG) Target URL (Signature): " + s);
                }

                return s;
        }
        return null;
    }
    
    public static String getListURL(Method method, HashMap<String, String> otherparams) throws UnsupportedEncodingException {
        String s;
        switch (method) {
            case Google:
                s = "http://video.google.com/videotranscript?frame=c&type=list&docid=" + otherparams.get("docid"); //+ id;
                System.out.println("(DEBUG) List URL: " + s);
                return s;
            // Subtitles only (until v0.5.6)
            //    s = "http://video.google.com/timedtext?type=list&v=" + id;
            //    System.out.println("(DEBUG) Tracks list URL: " + s);
            //    return s;
            case YouTubeLegacy: // Subtitles and translations (from v0.6) using "legacy method"
                s = "http://video.google.com/timedtext?type=list&tlangs=1&v=" + otherparams.get("v");
                System.out.println("(DEBUG) Tracks with targets list URL (Legacy): " + s);
                return s;
            case YouTubeSignature:
                /* ORIGINAL "Magic" URL example
                * http://www.youtube.com/api/timedtext?
                *      key=yttt1&
                *      hl=en_US&
                *      expire=1372005633&
                *      sparams=asr_langs,caps,v,expire&
                *      signature=4FE7A8E1FAAE338EAB840B58F3E05D1963F5550D.CE40D0149565FE4035DD4E914C144E864CE28302&
                *      caps=asr&
                *      v=L1hIAF5YvN0&
                *      asr_langs=ko,de,ja,pt,en,it,nl,es,ru,fr
                * 
                * REQUIRED URL result
                * http://www.youtube.com/api/timedtext?
                *      key=yttt1&
                *      expire=1372005633&
                *      sparams=asr_langs,caps,v,expire&
                *      signature=4FE7A8E1FAAE338EAB840B58F3E05D1963F5550D.CE40D0149565FE4035DD4E914C144E864CE28302&
                *      caps=asr&
                *      v=L1hIAF5YvN0&
                *      asr_langs=ko,de,ja,pt,en,it,nl,es,ru,fr&
                * 
                *      asrs=1&
                *      tlangs=1&
                *      type=list
                * 
               */        
                s = "https://www.youtube.com/api/timedtext" +
                       "?key=" + otherparams.get("key") +
                       "&expire=" + otherparams.get("expire") +
                       "&sparams=" + otherparams.get("sparams") +
                       "&signature=" + otherparams.get("signature") +
                       "&caps=" + otherparams.get("caps") +
                       "&v=" + otherparams.get("v") +
                       "&asr_langs=" + otherparams.get("asr_langs") +                       
                       "&asrs=1&type=list&tlangs=1";
            System.out.println("(DEBUG) ASR/tracks with targets list URL (Signature): " + s);
            return s;
        }
        return null;
    }
    
    public static String getMagicURL(String YouTubeWebSource) throws UnsupportedEncodingException {
        String result, s;
        String[] strings;
        
        // "ttsurl": "http:\/\/www.youtube.com\/api\/timedtext?key=yttt1\u0026hl=en_US\u0026expire=1372005633\u0026sparams=asr_langs%2Ccaps%2Cv%2Cexpire\u0026signature=4FE7A8E1FAAE338EAB840B58F3E05D1963F5550D.CE40D0149565FE4035DD4E914C144E864CE28302\u0026caps=asr\u0026v=L1hIAF5YvN0\u0026asr_langs=ko%2Cde%2Cja%2Cpt%2Cen%2Cit%2Cnl%2Ces%2Cru%2Cfr",
        strings = YouTubeWebSource.split("ttsurl");
        s = strings[1];
        strings = s.split(",");
        s = strings[0];
        strings = s.split("\"");
        s = strings[2];
        
        s = s.replace("\\/", "/");
        s = s.replace("\\u0026", "&");
        
        result = URLDecoder.decode(s, "UTF-8");
        
        return result;
    }
    
}
