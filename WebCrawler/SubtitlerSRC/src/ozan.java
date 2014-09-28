import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.util.List;
import java.util.MissingResourceException;
import java.util.Vector;


/**
 * The HelloWorldApp class implements an application that
 * simply prints "Hello World!" to standard output.
 */
class Ozan {
    TableModel tablemodelTracks, tablemodelTargets;
    private List<List<NetSubtitle>> lSubsWithTranslations;
    enum tIdioma {ca, en, es, it, pt_BR, zh_HanS, zh_HanT};
    public java.util.ResourceBundle bundle = java.util.ResourceBundle.getBundle("Bundle_en");

    public static void main(String[] args) {
	Ozan oz = new Ozan();
	String lN = args[0];
	String OF = args[1];
        System.out.println(lN); // Display the string.
        System.out.println("Upps"); // Display the string.
        System.out.println(OF); // Display the string.

	oz.initter();
	oz.retrieveSubtitles(lN,OF);
    }

    public void initter() {
        this.lSubsWithTranslations = new Vector<List<NetSubtitle>>(); this.lSubsWithTranslations.add(new Vector<NetSubtitle>()); this.lSubsWithTranslations.add(new Vector<NetSubtitle>());

        //this.setLanguage(bundle.getLocale().getLanguage());
        //this.jtfInput.setText(defaultURL);
        //this.jtfOutput.setText(defaultFileOut);
        
        //fc1.addChoosableFileFilter(new XMLFilter());
        //fc2.addChoosableFileFilter(new SRTFilter());

	}        



    public void retrieveSubtitles(String linkN,String OF) {
      InputStreamReader input = null;
	    System.out.println("AAA");

        String msg;        
        this.lSubsWithTranslations = new Vector<List<NetSubtitle>>();
        this.lSubsWithTranslations.add(new Vector<NetSubtitle>());
        this.lSubsWithTranslations.add(new Vector<NetSubtitle>());
        

       // Check if URL is valid
        try {
            lSubsWithTranslations = Network.getSubtitlesWithTranslations(linkN);
	    input = Network.readURL(lSubsWithTranslations.get(0).get(0).getTrackURL());	    
	    System.out.println(lSubsWithTranslations.get(0).get(0).getTrackURL());


        Converter conv = new Converter(input,OF,0);
        if (!conv.run()){ 
		System.out.println("Error Somewhere");
	}

	    //
            //prepareNewConversion();
            return;
        } catch (Exception e) {
	    System.out.println("Error");
            return;
        }
        
    }


}
