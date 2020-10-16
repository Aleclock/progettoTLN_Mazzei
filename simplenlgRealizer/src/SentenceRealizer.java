import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import simplenlg.features.*;
import simplenlg.framework.NLGFactory;
import simplenlg.lexicon.Lexicon;
import simplenlg.lexicon.italian.ITXMLLexicon;
import simplenlg.phrasespec.NPPhraseSpec;
import simplenlg.phrasespec.SPhraseSpec;
import simplenlg.phrasespec.VPPhraseSpec;
import simplenlg.realiser.Realiser;

public class SentenceRealizer {

        Lexicon lexIta = new ITXMLLexicon();
        NLGFactory nlgFactory = new NLGFactory(lexIta);
        Realiser realiser = new Realiser();

    public SentenceRealizer(JSONObject sentence) {}

    public String getRealisedSentence(JSONObject plan) {

        /** Create subject phrase**/

        JSONObject subjPred = (JSONObject) plan.get("subj");
        NPPhraseSpec subject = nlgFactory.createNounPhrase(subjPred.get("pred"));


        if (subjPred.get("num").equals("pl")) subject.setPlural(true);   // Number cordination
        if (subjPred.containsKey("gen")) {
            if (subjPred.get("gen").equals("f")) subject.setFeature(LexicalFeature.GENDER, Gender.FEMININE);
        }

        if (subjPred.containsKey("mod")) {
            JSONArray subjMod = (JSONArray) subjPred.get("mod");
            for (int i = 0; i < subjMod.size(); i++) {
                subject.addModifier(((JSONObject) subjMod.get(i)).get("pred"));
            }
        }

        /** Create verb phrase **/

        JSONObject verbPred = (JSONObject) plan.get("verb");
        VPPhraseSpec verb = nlgFactory.createVerbPhrase(verbPred.get("pred"));
        setVerbTense(verb, verbPred.get("tns").toString());

        if (verbPred.containsKey("mod")) {
            JSONArray verbMod = (JSONArray) verbPred.get("mod");
            for (int i = 0; i < verbMod.size(); i++) {
                verb.addModifier(((JSONObject) verbMod.get(i)).get("pred"));
            }
        }

        SPhraseSpec clause = nlgFactory.createClause(subject, verb); // Specify a sentence

        /** Create obj/compl phrase **/

        if (!plan.get("obj").toString().equals("{}")) {

            JSONObject objPred = (JSONObject) plan.get("obj");
            NPPhraseSpec obj = nlgFactory.createNounPhrase(objPred.get("pred"));

            if (objPred.get("num").equals("pl")) obj.setPlural(true);   // Number cordination

            // Insert obj modifier
            if (objPred.containsKey("mod")) {
                JSONArray objMod = (JSONArray) verbPred.get("mod");
                for (int i = 0; i < objMod.size(); i++) {
                    obj.addModifier(((JSONObject) objMod.get(i)).get("pred"));
                }
            }

            clause.setObject(obj);
        } else if (!plan.get("compl").toString().equals("{}")) {

            JSONArray compl = (JSONArray) plan.get("compl");

            for (int i = 0; i < compl.size(); i++) {
                JSONObject pred = (JSONObject) compl.get(i);
                clause.addComplement((String) pred.get("pred"));
            }
        }

        //System.out.println((clause.printTree("")));
        return realiser.realiseSentence(clause);
    }

    /**
     * Set verb tense
     * @param clause
     * @param tense
     */
    private void setVerbTense(VPPhraseSpec clause, String tense) {
        if (tense.equals("pres")) {
            clause.setFeature(Feature.TENSE, Tense.PRESENT);
        } else if (tense.equals("ger")) {
            clause.setFeature(Feature.PROGRESSIVE, true);
            clause.setFeature(Feature.PERFECT, false);
        }
    }
}
