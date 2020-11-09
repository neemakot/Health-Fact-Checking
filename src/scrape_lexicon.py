"""scrape_medical_terminology.py.
   Created on 25 April 2020.

   Acquire medical terms for use in filtering the claims data.
"""

import string
import requests
from bs4 import BeautifulSoup


def scrape_nhsconditions():
    """Scrape medical terms from NHS conditions page."""
    url = 'https://www.nhs.uk/conditions/#'
    response = requests.get(url, headers=None)
    tp_soup = BeautifulSoup(response.content, 'html.parser')

    return [str(li.get_text().strip()) + '\n' for li in
            tp_soup.find_all('li', {'class': 'nhsuk-list-panel__item'})
            ]


def scrape_everydayhealth():
    """Scrape medical terms from Everyday Health conditions page."""
    url = 'https://www.everydayhealth.com/conditions/'
    response = requests.get(url, headers=None)
    tp_soup = BeautifulSoup(response.content, 'html.parser')

    return [str(li.get_text().strip()) + '\n' for li in
            tp_soup.find_all(
                'li', {'class': 'topicslist__topiccolumncont-item'})
            ]


def scrape_medicalencyclopedia():
    """Scrape terms from MedlinePlus' medical encylcopedia."""
    ency_terms = []
    medencyclopedia_urls = [
        'https://medlineplus.gov/ency/encyclopedia_{}.htm'.format(letter)
        for letter in string.ascii_uppercase
        ]

    for url in medencyclopedia_urls:
        response = requests.get(url, headers=None)
        tp_soup = BeautifulSoup(response.content, 'html.parser')
        ency_terms += [str(li.get_text().strip()) + '\n' for li
                       in tp_soup.find('ul', {'id': 'index'}).find_all('li')]
    return ency_terms


def scrape_tlapcare():
    """Scrape hospital terms from TLAP Care and Support Jargon Buster."""
    content = ''.join(
        open('../../data/misc/TLAP Care and Support Jargon Buster.htm'
            ).readlines())
    tp_soup = BeautifulSoup(content, 'html.parser')

    return [str(li.get_text().strip()) + '\n' for li in
            tp_soup.find_all('a', {'class': 'term'})]


def scrape_nationalcareershealthcare():
    """"Scrape health care careers terms."""
    response = requests.get(
        'https://nationalcareers.service.gov.uk/job-categories/healthcare',
        headers=None
        )
    tp_soup = BeautifulSoup(response.content, 'html.parser')

    return [str(li.get_text().strip()) + '\n' for li in
            tp_soup.find_all('a', {'class': 'dfc-code-search-jpTitle'})]


def scrape_mayoclinic_terms():
    urls = []
    symptoms = []
    letters = string.ascii_uppercase + '0'
    symptoms_urls = ['https://www.mayoclinic.org/symptoms/index?letter={}'.format(
                     letter) for letter in letters]

    diseases_urls = ['https://www.mayoclinic.org/diseases-conditions/index?letter={}'.format(
                     letter) for letter in letters]

    procedures_urls = ['https://www.mayoclinic.org/tests-procedures/index?letter={}'.format(
                     letter) for letter in letters]

    drugs_urls = ['https://www.mayoclinic.org/drugs-supplements/index?letter={}'.format(
                     letter) for letter in letters]
    urls = symptoms_urls + diseases_urls + procedures_urls + drugs_urls

    for url in urls:
        response = requests.get(url, headers=None)
        tp_soup = BeautifulSoup(response.content, 'html.parser')

        if tp_soup.find('div', {'id': 'index'}) is None:
            continue
        if tp_soup.find('div', {'id': 'index'}).find('ol').get_text().strip() == '':
            continue 

        symptoms_links = [li.a['href'] for li in 
        tp_soup.find('div', {'id': 'index'}).find('ol').find_all('li')]

        symptoms += [url.split('/')[2].replace('-', ' ')+'\n' for url in symptoms_links]
    
    print(symptoms)
    print(len(symptoms))
    symptoms = sorted(list(set(symptoms)))
    with open('../../data/misc/terms_mayo_clinic.txt', 'w+') as output_file:
        output_file.writelines(symptoms)




def scrape_all():
    """Scrape all terms."""
    nhs_conditions = scrape_nhsconditions()
    # everydayhealth = scrape_everydayhealth()
    # medicalencyclopedia = scrape_medicalencyclopedia()
    # tlapcare = scrape_tlapcare()
    # nationalcareershealth = scrape_nationalcareershealthcare()

    # print("NHS:{0}\nEverydayhealth:{1}\nMedicalency:{2}\nTLAP:{3}\nCareers:{4}"\
    #     .format(len(nhs_conditions), len(everydayhealth),
    #             len(medicalencyclopedia), len(tlapcare),
    #             len(nationalcareershealth)
    #             )
    #      )

    return nhs_conditions
     # + everydayhealth + medicalencyclopedia + tlapcare + nationalcareershealth


def clean_and_save(terms):
    """Remove duplicates, save as text file."""    
 #    ignore_list = [ 'Review', 'Rights', 'ALL', 'sudden', 'unexpected', 'Vaccines',
 #    'Respect', 'Resilience', 'Liability', 'Discretion', 'Local offer',
 #    'Discrimination', 'Disengagement', 'Participation', 'Transition',
 #    'heavy', 'chronic', 'acute', 'Acute', 'high', 'low', 'insect', 'sudden', 
 #    'stopped or missed', 'lost/changed', 'burst', 'lost/changed', 'fits', 
 #    'early or delayed', 'early', 'excessive', '24h', "'I' statements", 
 #    'Suitable person', '5YFV', '22q11 deletion', 'sore', 'Zero harm', 'Wind', 
 #    'Welfare', 'Unconscious bias', 'Top-up fee', 'Time banks', 'Scrape',
 #    'Placement', 'Time out', 'Time outs', 'Shock', 'Shaking', 'Panel', 'Broker',
 #    'Service redesign', 'Service specification', 'Service user', 'Outputs',
 #    'Seven-day services', 'Prevention', 'Mapping', 'irregular', 'Monitor',
 #    'Market facilitation', 'Market management', 'Preventing falls', 'Blushing',
 #    'Market oversight', 'Market position statement', 'Resources',
 #    'Market shaping', 'Local area coordination', 'Discretionary services',
 #    'Localism', 'Locality commissioning', 'Fits', 'Falls', 'Beauty Toolbox',
 #    'Eligibility', 'Best interests', 'Best interests assessor', 'Pathway',
 #    'Best practice', 'Accelerated access collaborative', 'Financial assessment',
 #    'Accelerated access pathway', 'Access', 'Access to Work', 'Accountability', 
 #    'Active listening', 'Active participation', 'Active support', 
 #    'Activities of daily living', 'Advocacy', 'Advance decision', 'Inspection',
 #    'Advance statement', 'Agency', 'Agitation', 'Personal budget',
 #    'Alert', 'Assets', 'Assessment', 'Asset-based approach', 'Judicial review',
 #    'Asset-based community development', 'Asset-mapping', 'Pathologist',
 #    'Audit', 'Tailored support', 'Tariff income', 'Enforceability',
 #    'Benchmark', 'primary', 'Universal design', 'Prepayment card',
 #    'Universal information and advice', 'Support plan', 'Personalisation',
 #    'Universal personalised care', 'Universal services', 'Tendering', 
 #    'Support planning and brokerage service', 'Suitable person, Social capital',
 #    'Personal expenses allowance', 'Personal Independence Payment', 'Incidence', 
 #    'Personal assistant', 'People who use services', 'Any Qualified Provider',
 #    'Capabilities', 'Capacity', 'Challenging behaviour', 'Champion',
 #    'Change management', 'Chargeable services', 'Chills', 'Citizen advocate',
 #    'Citizens Advice', 'Client contribution', 'Client group', 'Compliance',
 #    'Confidentiality', 'Confusion', 'Aspiration', 'Barred list', 'Evaluation',
 #    'Case conference', 'Case finding', 'Case management', 'Domains', 'Duties',
 #    'Choice of accommodation', 'Commissioner', 'Commissioning', 'Inclusion',
 #    'Commissioning authority', 'Commissioning for Quality & Innovation',
 #    'Commissioning standards', 'Complement', 'Complement component 3',
 #    'Diversity', 'Enforcement action', 'Entitlement', 'Equity release' 'Provider',
 #    'Intervention', 'Stimulus', 'Co-commissioning', 'Co-design', 'Co-funding',
 #    'Co-location', 'Allocated case', 'Chronic', 'Debt recovery', 
 #    'Insidious', 'Innovation', 'Deferred payments', 'Diesel oil', 'Dignity',
 #    'Disproportionate', 'Dissect', 'Disposable income allowance', 'Enablement',
 #    'Erosion', 'Lateral', 'Mutuality', 'Re-assessment', 'Referral', 'Refraction',
 #    'Regulated financial advice', 'Regulator', 'Regulatory action', 'Scales', 
 #    'Shielding', 'Systemic', 'Weakness', 'braces', 'Reconfiguration', 'Protocol',
 #    'Procurement', 'Professional body', 'Outcomes', 'Outcomes framework', 'Outreach',
 #    'Deprivation of Liberty Safeguards', 'Deprivation of assets', 'Adequate security',
 #    'Authorised person', 'Exchange model', 'Failure to thrive', 'Capital limits'
 # ]

    terms_unique = {}

    for elem in terms:

        if elem in terms_unique:
            continue

        terms_unique[elem] = 1

        if elem.find("(") > -1:
            term = elem
            terms.remove(elem)
            first = term[:term.find("(")] + term[term.rfind(")")+1:]
            second = term[term.find("(")+1: term.rfind(")")]

            terms.append(first.strip() + '\n')
            terms.append(second.strip() + '\n')

    # terms = sorted(list(set([
    #     term for term in terms if term.strip() not in ignore_list])))

    with open('../../data/medical_event_claims/terms.txt', 'w+') as output_file:
        output_file.writelines(terms)


if __name__ == '__main__':
    # scrape_mayoclinic_terms()
    TERMS = scrape_all()
    clean_and_save(TERMS)
