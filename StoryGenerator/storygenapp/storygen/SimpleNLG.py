# java -cp lib/py4j0.6.jar:lib/simplenlg-3.8.jar:. Py4JServer 8080
from py4j.java_gateway import JavaGateway, GatewayClient, java_import

class SimpleNLG:

    def __init__(self):
        # Connect to Java Server to import SimpleNLG
        self.gateway = JavaGateway(GatewayClient(port=8080))
        self.importsimplenlg()

    def importsimplenlg(self):
        # Import the SimpleNLG classes
        java_import(self.gateway.jvm, "simplenlg.features.*")
        # java_import(self.gateway.jvm, "simplenlg.realiser.*")
        java_import(self.gateway.jvm, "simplenlg.framework.*")
        java_import(self.gateway.jvm, "simplenlg.lexicon.*")
        java_import(self.gateway.jvm, "simplenlg.phrasespec.*")
        java_import(self.gateway.jvm, "simplenlg.realiser.english.*")

        # Define aliases so that we don't have to use the gateway.jvm prefix.

        # Phrases
        self.NPPhraseSpec = self.gateway.jvm.NPPhraseSpec
        self.PPPhraseSpec = self.gateway.jvm.PPPhraseSpec
        self.VPPhraseSpec = self.gateway.jvm.VPPhraseSpec
        self.SPhraseSpec = self.gateway.jvm.SPhraseSpec
        self.AdvPhraseSpec = self.gateway.jvm.AdvPhraseSpec
        self.AdjPhraseSpec = self.gateway.jvm.AdjPhraseSpec

        self.NLGFactory = self.gateway.jvm.NLGFactory
        self.Realiser = self.gateway.jvm.Realiser

        # Verb Tenses
        self.TextSpec = self.gateway.jvm.TextSpec
        self.Tense = self.gateway.jvm.Tense
        self.Form = self.gateway.jvm.Form
        self.Feature = self.gateway.jvm.Feature

        # Instantiate Lexicon, Document Element, NLG Factory and Realiser
        self.DocumentElement = self.gateway.jvm.DocumentElement
        self.CoordinatedPhraseElement = self.gateway.jvm.CoordinatedPhraseElement
        self.LexicalCategory = self.gateway.jvm.LexicalCategory
        self.Lexicon = self.gateway.jvm.Lexicon
        self.lexicon = self.Lexicon.getDefaultLexicon()
        self.nlgfactory = self.NLGFactory(self.lexicon)
        self.realiser = self.Realiser(self.lexicon)