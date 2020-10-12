import org.json.simple.JSONObject;
import simplenlg.framework.*;
import simplenlg.lexicon.*;
import simplenlg.lexicon.italian.*;
import simplenlg.realiser.*;
import simplenlg.phrasespec.*;
import simplenlg.features.*;

import java.io.File;

// https://github.com/alexmazzei/SimpleNLG-IT/blob/master/docs/Testsimplenlgit.java#L10
public class Start {
    public static void main(String[] args) throws Exception {
        JSONReader jsonReader = new JSONReader();

        File[] dirListing = getFiles("/Users/aleclock/Desktop/uni/TLN/mazzei/progettoTLN_Mazzei/output/");

        if (dirListing != null) {
            for (File file : dirListing) {
                try {
                    //System.out.println("File: " + file.toString());

                    if (file.toString().toLowerCase().endsWith(".json")) {
                        // TODO verificare che finisca con .json
                        JSONObject plan = jsonReader.readJson(file);

                        SentenceRealizer realizer = new SentenceRealizer(plan);
                        String sentence = realizer.getRealisedSentence(plan);
                        System.out.println(sentence);
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        }
    }

    public static File[] getFiles(String path) {
        File dir = new File(path);
        return dir.listFiles();
    }

}