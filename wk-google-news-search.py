from pygooglenews import GoogleNews
import pandas as pd

def search_google_news(term, max_results=3):
    gn = GoogleNews(lang='es')  # Set the language to Spanish
    try:
        search_results = gn.search(f'"{term}"')
        return [(item['title'], item['link']) for item in search_results['entries'][:max_results]]
    except TypeError as e:
        if "unexpected keyword argument 'max_results'" in str(e):
            # Handle the case when 'max_results' is not supported
            search_results = gn.search(f'"{term}"')
            return [(item['title'], item['link']) for item in search_results['entries'][:max_results]]
        else:
            raise e

def main():
    search_terms = [
        "Extudia", "Inova Education", "Contact Chile Gestiones Interculturales LTD (WEP)", "Education USA",
        "Latino Australia Education Chile", "Viaja Estudia", "360 LIFE EXPERIENCE", "A Fondo Viajes y Turismo SAS",
        "AC Estudios En El Exterior", "Across Language Experts", "ADVANCE Idiomas", "AES International Education",
        "Ana Maria Pineda Maldonaldo Education Agent", "Andinoz Colombia Student Services",
        "Andres Felipe Garces Maya Education Agent", "Angelica Restrepo (Sole Trader)", "Anz International Education",
        "APICE", "Aussie You Too Pty Ltd", "Aussintech Studies Abroad", "Australasian Student Services",
        "Australia Group Study Travel Grow", "Australian Centre Bogota", "Australian Colombia Study Adventures",
        "Australian Education Option - Bucaramanga", "Australian International Student Office (AISO)",
        "Australian Option",
        "Babel Studies", "Be Global – Estudios en el Exterior", "Becas Para Colombianos", "Bizz Education",
        "Blue Studies",
        "Blue Studies Consultants Australia", "Boex Intercambios", "British Unlimited", "C. I. OZI International",
        "Caravan Travel", "Carlos Mario Hurtado Education Agent", "CEI", "Consejeria en Educacion Internacional",
        "Centro Colombo Americano", "Climbing Services", "Colombian School of Engineering Julio Garavito",
        "Columbus Agency",
        "CONEXION WORLD STUDIES", "Consejeria Britanica", "Cosmopolitan", "CSA Travels",
        "DG Australian Visas Education Agent", "Discover Study Travel", "Dunher Studies",
        "Easy Go International Students Agency", "Easy2Go", "EC2 Group", "Edex Educacion Por Excelencia",
        "EDU LINK Estudios en el exterior", "Educaminos", "Educamos Viajando", "Education Agency SAS",
        "Education and Migration Global Group", "Education First (EF)", "EDUCATION WORLD", "Education World Colombia",
        "Educaustralia", "Educonexion", "Edugroup", "Edumap", "EDUMIGRATION", "Edupi Australia", "EduPlanet",
        "EduTravel",
        "English Star", "Enter Corporation - Barranquilla", "Entre Idiomas", "Escalar Services- Bogota", "Escuela PCE",
        "Esenaus", "ESL Education Group", "ESL Estudios Internacionales", "Estudia en España",
        "Estudien Australia - Bucaramanga",
        "Estudios Internacionales", "ESTUVIAJE - Educación en el Exterior", "Experience estudios en el exterior",
        "Extudia",
        "FA Intercambios Estudiantiles", "Fex Juan Isaza & Asociados", "FLIPP Ciudadanos del Mundo",
        "Gea - Global Educational Access", "Global Connection", "Global Dreamers", "Global International Studies",
        "Global Learning Solutions", "Global Migration Services", "Global Study Partners Pty Ltd", "Globancy Pty Ltd",
        "GO GLOBAL International Education", "Go Study & Travel", "Go Study Australia Pty Ltd",
        "Go Study Work And Travel",
        "GoExperience SAS", "Going - Education International", "GOLDEN STUDIES", "GR Academic Exchange Programs",
        "Grasshopper International", "Grupo Gales", "Grupo Viva & Aprenda",
        "GSC Estudios en el Exterior (Global Studies Connection)", "GSC Studies Abroad", "GSlink Pty Ltd",
        "Holloway Institute",
        "ICCA-Sprach Institut", "IGSM SAS TA Brightdoors Education", "Ilt Escuela De Ingles", "Information Planet",
        "Instituto Nordico", "Intercambio de Idiomas", "Interlatina Colombia Student Exchange", "Interlingua Ltda",
        "Intern Group", "Internacional de Estudios", "International House - Bogota",
        "International Student Services Org",
        "Intersea - Bogota", "IS Link - International Student", "ISSO - International Student Services",
        "JAIME ANDRES SARMIENTO VELASCO Education Agent", "JD GLOBAL EXPERIENCE SAS",
        "Jennie Kent Education Consultant",
        "Jokum S.A.S", "JUAN CAMILO GUTIERREZ Education Agent", "Jump International Services",
        "KIOSK Estudios En El Exterior",
        "LAE Educacion Internacional", "LAE International Education", "LAE International Studies",
        "Language Tours Canada",
        "Latin Link Education Services", "Latino Australia Education", "LEARNING Educational Agency Barranquilla",
        "MAS Education", "Mate Education Colombia", "Mc Ewen And Howard", "MC WOMBAT STUDIES", "McEwen and Howard",
        "MI VISA AUSTRALIA-BOGOTA", "Migrate", "Migration and Studies Colombia SAS", "movUni Education Agent",
        "Mundo Destinos", "Mundo Experiencias", "Nueva Lengua", "O.W.L. Open World Learning", "Oceania Group SAS",
        "Olga Eusse Education Agent", "OZI International", "Pacific International Studies",
        "Pasaporte Estudios Education Agent",
        "PCT Colombia", "Pilar Howard Education Agent", "Planet Dreamers SAS Education Agent", "Planners Agency",
        "PortalUK Education Agent", "Primavera Camping Tours", "Proaction Migration Australia",
        "Royal Education International",
        "Servicio Educativo Internacional", "Sitio De Contacto", "Stanton School Of English", "Star Language",
        "STB Travelshop Agencia de Viagens e turismo LTDA", "STM Education Agent", "Student Advisors",
        "Student Colombia",
        "Student Connection", "Student Exchange Programs Sep", "Student Orbit Oz-Colombia", "Student Travel Centre",
        "Students Exchange Abroad Interna", "Studies Education", "Studies Planet", "Studio Travel Education Agent",
        "Study And Experience", "Estudios en el Exterior", "Study Buddy UK Education Agents", "Study Networks",
        "Study Now",
        "Study Overseas S.A.S", "STUDY UNION INTERNATIONAL", "Study Union International Colombia", "Study Unlimited",
        "StudyCo-Colombia", "Susana Carolina Romero Aparicio Education Agent", "Teaching & Tutoring",
        "Teaching And Tutoring College De Colombia", "Teduc Australia-Colombia", "TEDUCA Group",
        "Teducagroup Group Australia (Ofshore)", "Teducamos", "The Broad Club Education Agent",
        "The Grad School Education Agent",
        "The OM Education & Migration SAS (HQ)", "THREE FRIENDS STUDY ABROAD", "TLI Colombia", "Top Colleges",
        "Travelearners Estudios en el Exterior Education Agent", "Traveloop S.A.So",
        "Tres Amigos by Study Unlimited (Tres Amigos)", "Trotamundos S.A", "True Blue Education Australia",
        "U.Scholarship Advisers S.A.S", "ULPA - University Language Programs Abroad", "Universal Student",
        "Unlimited Australia",
        "UNO-800 STUDENT VISA", "UNO800", "Vedi Travel", "Vela Tours SAS", "Viaje Y Estudie",
        "Viajes & Viajes Medellin",
        "Viajes y Conexiones Education Agent", "Viajes y Viajes", "Viajes y Viajes Experience", "VIP STUDENT TRAVEL",
        "Viva Australia", "Volemi", "VT Education Education Agent", "WALES GROUP", "We Are TOP Education Agent",
        "WE International Studies Education Agent", "WINSTON SALEM", "Wombat Studies", "World Culture SAS",
        "World Experience Group", "World of Studies", "Yazmin Herrera Education Agent", "Yfu Colombia",
        "You Too Project",
        "Zully Matallana - Sole Trader Education Agent", "GLOBAL EDUCATION GLED ECUADOR S.A.", "The U for You Ecuador",
        "IE INTERCULTURAL EXPERIENCE", "BADA Education Group (Agent) - Lima", "BRIDGE BLUE PTY LTD - Arequipa",
        "Globancy Pty Ltd - Lima", "LAE", "AGM Education", "ASTEX", "Connectors Plus", "EAE Business School",
        "Edukonexion",
        "ENEB", "Interway", "INTO Intercambio Estudiantil (WEP)", "Latino Australia Education – Spain (Barcelona)",
        "Nomad Planet Experience", "OK Student", "Royal Universities", "SHE Herencia S.L (WEP)", "Timpany",
        "Tu futuro en Australia", "WHERE and WHAT", "Estudia Seguro", "GROW PRO", "Puerta Real", "Campus France",
        "GOPAL EDU JSC", "Latino Australia Education", "Estudie Canadá", "Contacto Canada", "CI Canada", "ILAC", "LSI",
        "Global Connection", "Un salto a Australia", "Edutravel International", "Nomadas", "Australia Study"
    ]

    results = []

    for term in search_terms:
        try:
            articles = search_google_news(term, max_results=3)
            count = len(articles)
            print(f'Search term: "{term}", Articles found: {count}')
            for title, url in articles:
                results.append({"Search Term": term, "News Title": title, "News Link": url})
        except Exception as e:
            print(f'Error occurred for search term: "{term}"')
            print(f"Error message: {str(e)}")

    df = pd.DataFrame(results)
    df.to_excel("google_news_spanish_exact_top3.xlsx", index=False)
    print("Results saved to google_news_spanish_exact_top3.xlsx")

if __name__ == "__main__":
    main()