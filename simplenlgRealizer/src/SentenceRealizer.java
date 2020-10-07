import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import simplenlg.features.Feature;
import simplenlg.features.NumberAgreement;
import simplenlg.features.Tense;
import simplenlg.framework.NLGFactory;
import simplenlg.lexicon.Lexicon;
import simplenlg.lexicon.italian.ITXMLLexicon;
import simplenlg.phrasespec.SPhraseSpec;
import simplenlg.realiser.Realiser;
import java.util.ArrayList;

public class SentenceRealizer {

        Lexicon lexIta = new ITXMLLexicon();
        NLGFactory nlgFactory = new NLGFactory(lexIta);
        Realiser realiser = new Realiser();

    public SentenceRealizer(JSONObject sentence) {

    }

    public String getRealisedSentence(JSONObject plan) {

        SPhraseSpec clause = nlgFactory.createClause();

        JSONObject subj = (JSONObject) plan.get("subj");
        JSONObject verb = (JSONObject) plan.get("verb");

        clause.setSubject(subj.get("pred"));
        clause.setVerb(verb.get("pred"));

        setVerbTense(clause, verb.get("tns").toString());


        if (!plan.get("obj").toString().equals("{}")) {
            JSONObject obj =  (JSONObject) plan.get("obj");
            clause.setObject(obj.get("pred"));
            clause.getObject().setFeature(Feature.NUMBER, NumberAgreement.PLURAL);

        } else if (!plan.get("compl").toString().equals("{}")) {
            JSONArray compl = (JSONArray) plan.get("compl");
            ArrayList pp = new ArrayList();

            for (int i = 0; i < compl.size(); i++) {
                JSONObject pred = (JSONObject) compl.get(i);
                clause.addComplement((String) pred.get("pred"));
            }
        }
        return realiser.realiseSentence(clause);
    }

    private void setVerbTense(SPhraseSpec clause, String tense) {
        if (tense.equals("pres")) {
            clause.setFeature(Feature.TENSE, Tense.PRESENT);
        } else if (tense.equals("ger")) {
            clause.setFeature(Feature.PROGRESSIVE, true);
            clause.setFeature(Feature.PERFECT, false);
        } else if (tense.equals("past")) {
            clause.setFeature(Feature.TENSE, Tense.PAST);
        }
    }
}
