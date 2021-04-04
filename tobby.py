# Suppressing Warnings
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import pandas as pd
import nltk
import string
from nltk.corpus import stopwords 
import re
import gensim, spacy, warnings
from collections import Counter
from nltk import word_tokenize, pos_tag
#from nltk import PorterStemmer
nltk.download('stopwords')
from gensim.utils import simple_preprocess
import matplotlib.pyplot as plt
import seaborn as sns
##Visualization on topic wise documents
import gensim.corpora as corpora
pd.set_option('display.max_colwidth', -1)
pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 100)
import streamlit as st
STOPWORDS=stopwords.words("english")

@st.cache

def get_data():
 path = r'C:\\Users\\YASHESWI MISHRA\\P40_G04_Dataset_Final.csv'
 return pd.read_csv(path)


df = get_data()

medicines = list(set(df['Medicine Name']))


medicine_name = st.sidebar.selectbox("Select medicine", options=[opt.strip() for opt in medicines])

#wait_meassge = "Please wait while analyzing the effectiveness of the medicine"

#keywords = ()

#if(len(medicine_name) > 0 and len(keywords)==0):
#    st.write(wait_meassge)

selected_medicine_df = df[df['Medicine Name']==medicine_name]


def deEmojify(inputString):
    return inputString.encode('ascii', 'ignore').decode('ascii') # A function to remove emojis from the reviews

def sentiment_category(rating):
    if (rating >= 5.0):
        return "positive"
    else:
        return "negative"

allowed_postags=['DET']    

def clean_text(text):
    #ps=PorterStemmer()
    
    text=deEmojify(text) # remove emojis
    text_cleaned="".join([x for x in text if x not in string.punctuation]) # remove punctuation
    
    text_cleaned=re.sub(' +', ' ', text_cleaned) # remove extra white spaces
    #text_cleaned = re.sub(r'\d+', '', text_cleaned)
    text_cleaned=text_cleaned.lower() # converting to lowercase
    tokens=text_cleaned.split(" ")
    tokens=[token for token in tokens if token not in STOPWORDS] # Taking only those words which are not stopwords
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(' '.join(tokens))
    lemmas = [token.lemma_ for token in doc if token.pos_ not in allowed_postags]
    text_cleaned=" ".join(lemmas)
    #text_cleaned=" ".join([ps.stem(token) for token in tokens])
    return text_cleaned    

def clean_text1(text): 
    delete_dict = {sp_character: '' for sp_character in string.punctuation} 
    delete_dict[' '] = ' ' 
    table = str.maketrans(delete_dict)
    text1 = text.translate(table)
    #print('cleaned:'+text1)
    textArr= text1.split()
    text2 = ' '.join([w for w in textArr if ( not w.isdigit() and  ( not w.isdigit() and len(w)>3))]) 
    return text2.lower()

# remove whitespace from text 
def remove_whitespace(text): 
    return  " ".join(text.split()) 

def remove_numbers(text): 
    result = re.sub(r'\d+', '', text) 
    return result

def remove_punctuation(text): 
    translator = str.maketrans('', '', string.punctuation) 
    return text.translate(translator) 

def text_lowercase(text): 
    return text.lower() 

med=df['Medicine Name'].unique()
med=','.join([str(elem) for elem in med])
med=med.replace('/','')
med=remove_numbers(med)
med=remove_whitespace(med)
med=med.replace('.','')
med=med.replace('-','')
med=text_lowercase(med)
med420=med.split(',')

##Cleaning condition column
selected_medicine_df.loc[selected_medicine_df['Condition']=='Diabetes, Type 2','Condition']='Diabetes, Type two'
selected_medicine_df.loc[selected_medicine_df['Condition']=='Diabetes, Type 1','Condition']='Diabetes, Type one'
selected_medicine_df['Condition']=selected_medicine_df['Condition'].apply(str)
selected_medicine_df['Condition']=selected_medicine_df['Condition'].apply(remove_numbers)
selected_medicine_df['Condition']=selected_medicine_df['Condition'].replace(to_replace='</span> users found this comment helpful.',value=np.nan)

cond=selected_medicine_df['Condition'].unique()
cond=','.join([str(mellow) for mellow in cond])
cond=cond.replace('/','')
cond=remove_numbers(cond)
cond=remove_whitespace(cond)
cond=cond.replace('.','')
cond=cond.replace('-','')
cond=text_lowercase(cond)
cond=re.sub("\s+", ",", cond.strip())
cond420=cond.split(',')

def remove_stopwordzz(text):
    textArr = text.split(' ')
    rem_text = " ".join([i for i in textArr if i not in set(stop_words)])
    return rem_text
stop_words=stopwords.words('english')
add=['ive','tried','id','mg','else','panty','long','hope','quotpsychiatristquot','announce','seem','name','well','please','thank','medicine','start','couple','list','full','psy','anxietypanic','physicians','well','review','link','unwell','effect','peace','weight gain','positive','trial','third','reason','adjust','wish','quotbaker','happen','quotstressquot','parent','people','peoples','cost','manufacture','quotmedicationquot','advice','foward','medication','holiday','psychiatrist','meeting','feel', 'actquot','quotfull','drugquot','dept','offer','quotit','error','crap','quote','pron','quot','quotdocsquot','quotstressquot''eventuallyquot''quotmedicationquot','waste','money','thought','wake','formula','obtain','walgreen','course','refer','end','think','tolerance','yestreday','remove','today','intolerable','amount','pharmaceutical','bottle','sheriff','sideaffect','say','tell','phamacist','contact','thing','ingredient','bright','total','try','middle','crazy','sound','main','find','immediately','breakfast','switch','liner','college','initially','walk','kitchen','family','masters','blue','color','colour','prescribe','term','female','confused','leave','almost','answer','life','really','even','took','good','pass','like','plan','though','also','tell','pill','condom','recommend','anyone','hour','later','test','come','boyfriend','wife','doc','quot quot','normal','ever','quot','decide','went','weeks','don ’','’ve','"m',"'ve","'m",'i ’','&quot',
         'I ’','’ t','side','effects','teacher','difference','eliminate','anxiety','house','care','never','improvement','daily','something','dosage','dose','sure','next','december','july','june','decided','go','gone','much',
         'many','taken','many','done','first','last','shows','june','july','january','mgs','because','went','asap','however','instead','experience','illness','person','along',
             'med','im','would','could','still','wait','morning','entire','put','one','day','month','within','whole','time','work','want','since','happy','eat','gain','lb','lbs','food','persist','touch',  
             'tried','whole','using','use','every','night','taking','take','get','got','year','week','mirtazapine','mesalamine','prescribed','hospitalise','fine','progressive','combo','particular','quotgraduatedquot',
             'bactrim','put','away','second','august','little','march','make','january','august','november','october','thru','quottolerancequot','keep','simply','attack','drug','punch',
             'september','doctor','th','couldnt','april','friday','mgs','help','make','use','hill','stay','afganistan','s','know','hes','drs','different','event','black','working','tend','ptsd','wean','wall','claire','contrave','cyclafem ','zyclara','copper','amitriptyline','methadone','levora','suicidaluse','manage','withdraws','benzo',
             'paroxetine','miconazole','belviq','seroquel','ambien','nuvigil','chantix','microgestin fe ','klonopin','actos','nothing','symptom','brother','quite','realize','realise','couch',
             'ciprofloxacin','trazodone','enteragam','aripiprazole','cyclosporine','suprep bowel prep kit','movantik','lorcaserin','twice','worth','kind',
             'oxybutynin','lurasidone','clonazepam','ciclopirox','sodium oxybate','lamotrigine','blisovi fe ','ivermectin','nearlysuccessful','youre','approx','effective',
             'duloxetine','nuvaring','escitalopram','tesamorelin','campral','gabapentin','levonorgestrel','aubra','plan b onestep','benzos','maintainence','basis',
             'ethinyl estradiol etonogestrel','microgestin fe  ','wellbutrin','benzoyl peroxide clindamycin','etonogestrel','constantly','chaos','gogogo','assistant','asisstant','consider',
             'nitrofurantoin','ortho tricyclen lo','tamsulosin','hospitalise','hospitalized','hospitalised','business','associate','tofacitinib','cryselle','amphetamine dextroamphetamine',
             'clindamycin','pramipexole','skyla','lastacaft','effexor xr','nifedipine','afrezza','zoloft','ziprasidone','brand','restore','partly','decade',
             'ethinyl estradiol norethindrone','sertraline','aluminum chloride hexahydrate','paragard','acetaminophen hydrocodone','maintenance','force','lbsmi','nonexistent','effectiveness','effective',
             'pregabalin','ethinyl estradiol levonorgestrel','ultram','phentermine','venlafaxine','buspar','great','instruct','progressively','reasonably','careful','carefully',
             'aviane','inderal','promethazine','tioconazole','orthovisc','implanon','marezine','minoxidil','humira','eventok','caution','research',
             'insulin inhalation','rapid acting','day','days','guaifenesin pseudoephedrine','phentermine topiramate','pristiq','depression',
             'month','months','year','years','phenazopyridine','clonidine','ethinyl estradiol norgestimate','nicoderm cq','build','close','especially','emotional',
             'celecoxib','fluoxetine','topamax','depakote','riboflavin','lo loestrin fe','drospirenone estradiol','bupropion','bacitracin neomycin polymyxin b','yaz','jolessa',
             'oxycodone','nexplanon','brisdelle','beyaz','yasmin','nucynta er','prozac','kariva','liraglutide','sutent',
             'tramadol','tylenol with codeine #','magnesium citrate','depoprovera','insist','eventuallyquot','husband','kid',
             'drospirenone ethinyl estradiol','safyral','desyrel','glyburide','aldesleukin','desvenlafaxine','healthcare','company','prescribing','perfect','sure','quotnumbquot','bother',
            'acamprosate','spironolactone','doxylamine pyridoxine','demerol','vyvanse','sovaldi','motrin ib','valacyclovir',
            'buprenorphine naloxone','metoprolol','montelukast','dextromethorphan','levitra','restoril','azathioprine','depressionquot','toll','system','thrown','always','quotthe',
            'adapalene benzoyl peroxide','linzess','levetiracetam','ziana','suboxone','tinidazole','diazepam','quetiapine',
            'acetaminophen butalbital caffeine','estradiol','propofol','propranolol','levofloxacin','vilazodone','accutane','nalbuphine',
            'lexapro','miralax','phenobarbital','trisprintec','metronidazole','imiquimod','caffeine','lisinopril','benzonatate','opiate',
            'ayr saline nasal','clarithromycin','enbrel','polyethylene glycol with electrolytes','beware','without','quotangerquot',
            'restasis','symbyax','tretinoin','gleevec','ropinirole','clomiphene','clotrimazole','topiramate','fluorouracil','genvoya','tessalon perles','doctors','lucid','kick','endeavor','stand',
            'asenapine','adipexp','prenatal plus','keflex','vitamin d','flexeril','viibryd','lysteda',
            'omnicef','augmentin','pentasa','zofran','kapidex','serzone','hyoscyamine methenamine methylene blue phenyl salicylate',
            'diphenhydramine','minocycline','monistat day combination pack','pitocin','pyridostigmine','naprosyn','elocon','result','throughout','point',
            'pazopanib','denosumab','bisacodyl','paxil','methotrexate','sprintec','buprenex','apri','relate','breakup','relationship','wrong',
            'benzoyl peroxide erythromycin','qsymia','lyrica','trintellix','oseltamivir','seasonique','niravam','celexa','personally','normally','grain','salt','success',
            'codeine guaifenesin','cefuroxime','ortho evra','xanax','ondansetron','dulaglutide','supartz','naproxen','right','changed','drive','ruin','everywhere',
            'alesse','orlistat','methylprednisolone','cymbalta','aspirin carisoprodol','canagliflozin','nasonex','junel fe ','uniquely','fish','must','water','hole','mindfull','mountain','bike','prior','wildly','either',
            'kombiglyze xr','pegfilgrastim','azelaic acid','mirena','suvorexant','lysine','nexium','citalopram','drysol','corticotropin',
            'meclizine','cefdinir','methocarbamol','azithromycin','sinemet','esomeprazole','prednisone','fentanyl','pseudoephedrine','hell','hotcold','emotionally','really',
            'risperidone','alpha proteinase inhibitor','junel fe  ','divalproex sodium','pravastatin','vardenafil','abilify','amlodipine',
            'carvedilol','xyzal','budeprion sr','rosuvastatin','victoza','percocet','trulicity','tranexamic acid','paxil cr','oxycontin',
            'chlordiazepoxide','olanzapine','doxycycline','cellcept','imodium ad','cobicistat elvitegravir emtricitabine tenofovir alafenamide',
            'chateal','rizatriptan','strattera','monistat day combination pack','cyclobenzaprine','ethinyl estradiol norelgestromin','antidepressant','need',
            'uptravi','eletriptan','isotretinoin','rosula','methyldopa','fetzima','linaclotide','arimidex','eszopiclone','mononessa','wonderful','restaurant','kindergarden','postpartum','quotbrain','zapsquot',
             'norethindrone','medroxyprogesterone','synviscone','xulane','remeron','pamelor','orphenadrine','etanercept','bupropion naltrexone',
             'milnacipran','acetaminophen codeine','penicillin v potassium','varenicline','advair diskus','cialis','tadalafil','alprazolam',
     'desogestrel ethinyl estradiol','metformin','duofilm','sprycel','ella','sronyx','alcaftadine','sulfamethoxazole trimethoprim','levothyroxine','kineret',
     'naturethroid','cholestyramine','flector patch','prochlorperazine','zovia','toprolxl','perampanel','cozaar','white','someone','entirely','numerous','ahead','pleased',
     'acetaminophen dexbrompheniramine pseudoephedrine','wayyes','guess','itbut','therefore','support','holy','area','noven',
     'androgel','avinza','ativan','atomoxetine','oxymorphone','saphris','mirabegron','pramoxine','alphagan p','fact','trust','mequot','afterward','neighborhood',
     "phillips' milk of magnesia",'eluxadoline','terbinafine','indomethacin','latuda','plan b','apremilast','norco','savella','originally','yo',
     'vivitrol','ortho cyclen','advair hfa','anastrozole','xarelto','metformin sitagliptin','belsomra','trinessa','prazosin',
     'dicyclomine','sodium hyaluronate','toradol','epiduo','kyleena','levsin sl','human papillomavirus vaccine','free','loud','treatment','pretty',
     'lortab','dexmethylphenidate','catapres','harvoni','lansoprazole','carbidopa levodopa','hydrocodone','morphine','relistor','depressant','prescription','manifestation','regret','frequency',
     'bevacizumab','barium sulfate','azor','azelastine fluticasone','zoster vaccine live','diltiazem','triprevifem','dapsone','sing','birthday','ask','spend',
     'bismuth subsalicylate','wellbutrin xl','carisoprodol','olopatadine','citric acid magnesium oxide sodium picosulfate',
     'relpax','dalfampridine','dilantin','leuprolide','cetirizine','macrobid','methylphenidate','nitroglycerin','ritalin',
     'exubera','hydroxychloroquine','loestrin fe','enskyce','stalevo','amerge','lorazepam','lubiprostone','simcor','avonex pen',
     'methadose','acetaminophen oxycodone','abacavir dolutegravir lamivudine','give','remember','talk','able','mention','easy',
     'sumatriptan','cambia','tizanidine','adderall','exalgo','guaifenesin','ketorolac','tegretol','vesicare','plavix','wonder','billing','importantly','hopelessness','roof','friend','partner','pet','plug','bout','vortioxetine','atorvastatin','dienogest estradiol','roflumilast','minastrin fe','diclofenac','opana','donnatal','pm','exact','servere','mean',
     'depakote er','donepezil','sofosbuvir','monistat ','zolpidem','horizant','brovana','dulcolax','tylenol pm','saxenda','sulfasalazine',
     'nicotine','reglan','seroquel xr','dulera','mibelas fe','naltrexone','portia','temazepam','clindamycin tretinoin','quotbraiin','read','reviews','headachessensitive',''
     'meperidine','hydroxyzine','ethinyl estradiol norgestrel','dapagliflozin','myrbetriq','hysingla er','propafenone','lunesta','liletta','trimethoprim','ortho micronor',
     'prevacid','onabotulinumtoxina','aptensio xr','omeprazole','finasteride','rapaflo','duexis','tamiflu','rozerem','department','effort','besides','episode',
     'synthroid','differin','doxepin','acetaminophen dichloralphenazone isometheptene mucate','crestor','narcan injection','sildenafil',
     'lipitor','macrodantin','intuniv','pantoprazole','keppra','keppra xr','acyclovir','ledipasvir sofosbuvir','metrocream',
     'copaxone','magnesium sulfate potassium sulfate sodium sulfate','armodafinil','fluconazole','tylenol','quantity','neighbourhood','society','fortune','magic','setraline',
     'larin fe','xiidra','levaquin','tacrolimus','luvox','lotrel','conjugated estrogens medroxyprogesterone','amazing','group','creative','male','mother','father','worry','mall',
     'nortriptyline','adderall xr','viberzi','evolocumab','triumeq','gabapentin enacarbil','glucophage','unable','may','truequot',
     'soma','antipyrine benzocaine','liothyronine','docosanol','qtapp dm','valium','effexor','efavirenz',
     'chlorpheniramine hydrocodone pseudoephedrine','lutera','zoladex','keytruda','roxicodone','phenergan','buspirone','empagliflozin linagliptin','singulair',
     'viagra','rituxan', 'jublia', 'fluticasone vilanterol', 'fentanyl transdermal system', 'diclegis','luck','provider','negatively','whiskey',
     'hydromet','zipsor', 'milk of magnesia', 'melatonin', 'moviprep', 'aczone',' quotbadquot','extremely','helloi',
     'lactulose','pioglitazone','desloratadine','entyvio','gefitinib','meloxicam','bronkaid','niacin','paliperidone',
     'drospirenone ethinyl estradiol levomefolate calcium','scopolamine','sterapred','amoxicillin clavulanate','pentosan polysulfate sodium',
    'hydromorphone','flurazepam','zutripro','fluticasone','vicodin','mirapex','mometasone','fioricet','story','ongoing','shoot','figure','suppose','approximately',
     'metoclopramide','milk thistle','lidocaine','metaxalone','glatiramer','tecfidera','benzocaine','ustekinumab',
     'mucinex','adalimumab','tiotropium','vascepa','lisdexamfetamine','naloxegol','ixekizumab','mirvaso','sit','settle','consume','population','idiot','turkey',
     'estarylla','ortho tricyclen','ramipril','aranesp','zioptan','zohydro er','rifaximin','hyoscyamine','clarity','exercise',
     'zovirax cream','teriparatide','ammonium lactate halobetasol','atenolol','testosterone','promising','hate','suddenly',''
     'cobicistat elvitegravir emtricitabine tenofovir','ethinyl estradiol ethynodiol','embeda','duac','infliximab','cease','sky','best','hope','duty','cloud','appreciate','motivation','spectrum',
     'deplin','penciclovir','lupron depot','avelox','geodon','cogentin','mefenamic acid','pramosone','synalar ointment',
     'emsam','doryx','ranolazine', 'hylenex', 'cosentyx', 'medrox', 'cipro', 'oxcarbazepine', 'tapentadol', 'cytomel','twelve','anything','improve','order','decision','incredibly',
     'gildess fe ', 'terconazole', 'pneumococcal valent vaccine','intrusive','outweigh','unfortunately','alcohol','lexipro','times','home','promise','okay','ok',
     'eflornithine', 'etodolac', 'rabeprazole', 'librax', 'hydrochlorothiazide', 'pradaxa', 'kava', 'focalin xr',
     'levlen', 'femara', 'migranal', 'gianvi', 'flonase', 'stendra', 'dilaudid', 'exenatide','upset','completely','pfizer','molecular','devastating','horrifying',
     'risperdal', 'teriflunomide', 'esterified estrogens methyltestosterone','three','finally','let','army','part','terrify','force',
     'loratadine pseudoephedrine', 'azithromycin dose pack', 'pylera', 'protonix iv','currently','hopefully','suggest','following','anymore','process','step','minute','sooner',
     'vraylar', 'adapalene', 'camrese', 'gavilyten', 'dimenhydrinate', 'microgestin ', 'midazolam','push','check','everything','scare','become','call',
     'moxifloxacin', 'multivitamin with minerals', 'amoxicillin', 'butrans', 'lamictal', 'clomid','five','notice','open','old','fearless','opposite',
     'spiriva', 'requip', 'celebrex', 'nasacort allergy hr','scared','stack','stuck','market','sometimes','share','negative','learn','robot','desire',
     'metformin saxagliptin', 'bunavail', 'soolantra', 'acetaminophen aspirin caffeine', 'halcion','store','impact','regular','message','awesome','history','plus',
     'ramelteon','invokana','colesevelam','fulvestrant','several','change','overall','depressive','session','depressed','writing','believe',
     'natalizumab','benicar','loseasonique','lifitegrast','hycodan','icosapent','azelastine','efinaconazole','benzodiazepine','solution','tranquilizer','unexpectedly','include','live',
     'loratadine','rexulti','sanctura','clozapine','benadryl allergy','luminal','tolterodine','benadryl','insulin lispro',
     'albuterol','sucralfate','mydayis','fluocinolone','biotin','ocella','bromfed dm','losartan','lasix','itraconazole','miss','eventually','attempt',
     'methylnaltrexone','cutivate', 'cyred', 'breo ellipta', 'limbrel', 'prilosec','talwin nx', 'concerta', 'praluent', 'tarceva', 'farxiga', 'halobetasol','anxious','frighten','convenience','pray','clean',
     'biaxin', 'kenalog', 'thyroid desiccated', 'naproxen sumatriptan', 'botox', 'guanfacine','helpful','clearly','move','addition','therapist','heaven','sadly','recently','firstly',
     'vimpat', 'fenofibrate', 'ezgas ii', 'intelence', 'chlorpheniramine hydrocodone', 'ertaczo','minipress','hospitalize','mile','child',
     'amethyst', 'sensipar', 'lupron', 'furosemide', 'phendimetrazine', 'asacol','provigil', 'sulfacetamide sodium', 'zoledronic acid', 'claravis', 'cyanocobalamin',
     'aleve', 'alprostadil', 'flagyl', 'clopidogrel', 'gildess fe  ', 'astelin','atropine hyoscyamine phenobarbital scopolamine', 'aldactone', 'altabax',
     'seasonale', 'amlodipine olmesartan','pron', 'invega', 'rituximab', 'delsym', 'selegiline', 'fastin','half','add','promising','monitor',
     'larin fe ', 'amphetamine', 'buprenorphine', 'fleet enema', 'yuvafem', 'lodine', 'mgday','instantly','towards','ton','past','hospital',
     'kinda','walmart','ve','ssris','zaps','fesoterodine','xylometazoline','cyproheptadine','quotbadquot','lutuda','somewhat','quottrie','level',
     'benzoic acid salicylic acid','adalat cc','methylergonovine','vistaril','chlordiazepoxide clidinium','taytulla','zyrtec','aware','security','wear',
     'tysabri','hylan gf ','tussionex pennkinetic','jalyn','excedrin back & body','polyethylene glycol ','phosphorated carbohydrate solution',
     'lamisil','neupro','brimonidine timolol','supprelin la','miconazole zinc oxide','noticeable','compare','hold','book','soon','aposetraline',
    'zubsolv','aspirin butalbital caffeine','senna','denavir','dhe ','beclomethasone', 'neurontin', 'robaxin','around','probably','complied',
     'thorazine','bydureon','meridia','fiorinal','carbamazepine','multivitamin',' prenatal','nivolumab','hetlioz','crisaborole','mono','tremendously','impure',
     'tazorac','lomotil','oxytrol','zaleplon','disulfiram','loestrin ','silodosin','fiorinal with codeine','elmiron','lithium','obnoxious','beg','miserable','apparently',
     'levophed','remicade','gilenya','reclipsen','atripla','droperidol','trihexyphenidyl','estropipate','podofilox','symbicort',
     'xerac ac','maxaltmlt','fluticasone salmeterol', 'propulsid', 'aricept', 'nebivolol', 'simvastatin','actually','understand','existant','existent',
     'tradjenta', 'zomigzmt', 'colchicine', 'dasatinib', 'ventolin hfa', 'aciphex', 'imipramine', 'nodoz','shit','stuff','google',
     'ciprofloxacin dexamethasone','tricor','elavil','snris','zombie','enoxaparin','lovastatin','&#039'] 
stop_words.extend(add)
stop_words.extend(cond420)
stop_words.append(medicine_name)
stop_words.append(medicine_name.lower())
stop_words.append(medicine_name.upper())
stop_words.append(medicine_name.title())



selected_medicine_df['review_category']= np.where(selected_medicine_df['Ratings']>=5.0,'positive','negative')
selected_medicine_df['Reviews']=selected_medicine_df['Reviews'].apply(lambda x:x.strip('\n')) 
selected_medicine_df['cleaned_reviews'] =selected_medicine_df['Reviews'].apply(clean_text)
selected_medicine_df['cleaned_reviews'] =selected_medicine_df['cleaned_reviews'].apply(clean_text1)
selected_medicine_df['cleaned_reviews'] =selected_medicine_df['cleaned_reviews'].apply(remove_numbers)
selected_medicine_df['cleaned_reviews'] =selected_medicine_df['cleaned_reviews'].apply(remove_whitespace)
#selected_medicine_df['cleaned_reviews'].tolist()
selected_medicine_df['cleaned_reviews']=selected_medicine_df['cleaned_reviews'].apply(remove_stopwordzz)
#selected_medicine_df['cleaned_reviews'].tolist()


pole=','.join([str(i) for i in selected_medicine_df['cleaned_reviews']])
pole=pole.replace('-PRON-',"")
pole=pole.replace('-pron-',"")


column_names = ['Review']
positive_reviews_df = pd.DataFrame(columns = column_names)
positive_reviews=selected_medicine_df.loc[selected_medicine_df['review_category']=='positive','cleaned_reviews'].tolist() # extracting all positive reviews and converting to a list
positive_reviews_df =  pd.DataFrame(positive_reviews,columns = column_names)

negative_reviews_df = pd.DataFrame(columns = column_names)
negative_reviews=selected_medicine_df.loc[selected_medicine_df['review_category']=='negative','cleaned_reviews'].tolist() # extracting all positive reviews and converting to a list
negative_reviews_df =  pd.DataFrame(negative_reviews,columns = column_names)


def getMostCommon(reviews_list,topn=40):
    reviews=" ".join(reviews_list)
    tokenised_reviews=reviews.split(" ")
    
    
    freq_counter=Counter(tokenised_reviews)
    return freq_counter.most_common(topn) # return words with the highest frequencies

def plotMostCommonWords(reviews_list,topn=40,title="Common Review Words",color="blue",axis=None): #default number of words is given as 20
    top_words=getMostCommon(reviews_list,topn=topn)
    data=pd.DataFrame()
    data['words']=[val[0] for val in top_words]
    data['freq']=[val[1] for val in top_words]
    if axis!=None:
        sns.barplot(y='words',x='freq',data=data,color=color,ax=axis).set_title(title+" top "+str(topn))
    else:
        sns.barplot(y='words',x='freq',data=data,color=color).set_title(title+" top "+str(topn))


from nltk import bigrams
lines = map(str.split,pole.split(','))
red=[]
for line in lines:
    red.append(", ".join([" ".join(bi) for bi in bigrams(line)])) 
blue=[]
for i in red:
    blue.append(i.split(','))       



###Building LDA model
dictionary = corpora.Dictionary(blue)
corpus= [dictionary.doc2bow(rev) for rev in blue]


LDA = gensim.models.ldamodel.LdaModel

# Build LDA model
lda_model = LDA(corpus=corpus, id2word=dictionary, num_topics=3,chunksize=100, passes=45,iterations=150)   



##What is the Dominant topic and its percentage contribution in each document
data=negative_reviews_df['Review'].tolist()
def format_topics_sentences(ldamodel=None, corpus=corpus, texts=data):
    sent_topics_df = pd.DataFrame()
    for i, row_list in enumerate(ldamodel[corpus]):
        row = row_list[0] if ldamodel.per_word_topics else row_list      
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:
                 wp = ldamodel.show_topic(topic_num)
                 topic_keywords = ", ".join([word for word, prop in wp])
                 sent_topics_df = sent_topics_df.append(pd.Series([int(topic_num), round(prop_topic,4), topic_keywords]), ignore_index=True)
            else:
                break
                    
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']
    
    contents = pd.Series(texts)
    sent_topics_df = pd.concat([sent_topics_df, contents], axis=1)
    return(sent_topics_df)

df_topic_sents_keywords = format_topics_sentences(ldamodel=lda_model, corpus=corpus, texts=blue)

df_dominant_topic = df_topic_sents_keywords.reset_index()
df_dominant_topic.columns = ['Document_No', 'Dominant_Topic', 'Topic_Perc_Contrib', 'Keywords', 'Text']
#df_dominant_topic

st.title("MEDICINE EFFECTS ANALYZER")
keywords =  set(df_dominant_topic['Keywords'])

if (len(keywords) > 0 ):
 st.write("Side Effects :",keywords)


##Wordcloud of Top N words in each topic
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors

cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]  

cloud = WordCloud(stopwords=set(),
                  background_color='white',
                  width=2500,
                  height=1800,
                  max_words=100,
                  colormap='tab10',
                  color_func=lambda *args, **kwargs: cols[i],
                  prefer_horizontal=1.0)

topics = lda_model.show_topics(formatted=False)

fig, axes = plt.subplots(1, 2, figsize=(10,10), sharex=True, sharey=True)

for i, ax in enumerate(axes.flatten()):
    fig.add_subplot(ax)
    topic_words = dict(topics[i][1])
    cloud.generate_from_frequencies(topic_words, max_font_size=300)
    plt.gca().imshow(cloud)
    #plt.gca().set_title('Side Effects ' + str(i+1), fontdict=dict(size=16))
    plt.gca().axis('off')


plt.subplots_adjust(wspace=0, hspace=0)
plt.axis('off')
plt.margins(x=0, y=0)
plt.tight_layout()
st.pyplot(fig)




conditions =  list(set(selected_medicine_df['Condition']))
conditionDict = {} 
for x in conditions:
    np.where(selected_medicine_df[selected_medicine_df['Condition']==x])
    condition,reviews = x,selected_medicine_df[selected_medicine_df['Condition']==x]['review_category'].value_counts()
    conditionDict[condition] = reviews
    
effectiveness_df = pd.DataFrame(conditionDict)
effectiveness_df = effectiveness_df.T
effectiveness_df['Condition' ] = effectiveness_df.index
effectiveness_df = effectiveness_df.reset_index(drop=True)
effectiveness_df.fillna(0,inplace=True) 

if(effectiveness_df.shape[0]>0):
 col_names =  effectiveness_df.columns 
 if('negative' not in col_names) : 
     effectiveness_df['negative'] = 0
 if('positive' not in col_names) : 
     effectiveness_df['positive'] = 0    
     
 effectiveness_df['Effectiveness %'] = np.round(effectiveness_df['positive']/(effectiveness_df['negative']+effectiveness_df['positive'])*100,2)
 st.write('Effectiveness :', effectiveness_df[['Condition','Effectiveness %']])  
 
 
 
#import pyLDAvis.gensim
#pyLDAvis.enable_notebook()
#vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary=lda_model.id2word)
#st.pyplot(vis)
    