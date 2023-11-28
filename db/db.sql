CREATE DATABASE micro_lecturi;
USE micro_lecturi;

CREATE TABLE `user` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `enabled` BOOLEAN NOT NULL
);

CREATE TABLE `user_verification` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_user` INT NOT NULL,
    `token` VARCHAR(255) NOT NULL UNIQUE,
    `active_date` DATETIME NOT NULL,
    FOREIGN KEY (`id_user`) REFERENCES `user`(`id`)
);

CREATE TABLE `lecture_category` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE `lecture` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `author` VARCHAR(255) NOT NULL,
    `description` VARCHAR(5000) NOT NULL, -- Added this line
    `chunks` INT NOT NULL,
    `id_category` INT NOT NULL,
    FOREIGN KEY (`id_category`) REFERENCES `lecture_category`(`id`)
);

CREATE TABLE `subscription` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `id_user` INT NOT NULL,
    `id_lecture` INT NOT NULL,
    `start_date` DATETIME NOT NULL,
    `current_chunk` INT NOT NULL,
    `is_active` BOOLEAN NOT NULL,
    FOREIGN KEY (`id_user`) REFERENCES `user`(`id`),
    FOREIGN KEY (`id_lecture`) REFERENCES `lecture`(`id`)
);

INSERT INTO `lecture_category` (`name`) VALUES
    ('Epic'),
    ('Liric'),
    ('Dramă'),
    ('Populare');

    -- epic
INSERT INTO `lecture` (`title`, `author`, `description`, `chunks`, `id_category`) VALUES
    ('Ion', 'Liviu Rebreanu', 'Romanul "Ion" este o operă fundamentală a literaturii române, urmărind povestea lui Ion, un tânăr care își dorește pământ mai mult decât orice. Acesta este dispus să renunțe la iubirea adevărată pentru a obține pământul dorit, ceea ce pune în lumină legătura strânsă dintre om și pământ în contextul vieții rurale românești.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Ultima noapte de dragoste, întâia noapte de război', 'Camil Petrescu', 'Opera se remarcă prin introspecția psihologică, prezentând dilemele și conflictele interioare ale personajului principal, Ștefan Gheorghidiu. Romanul explorează temele trădării, geloziei și realităților brutale ale războiului, în contextul Primului Război Mondial.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Moromeții I', 'Marin Preda', 'O capodoperă a literaturii române, "Moromeții" descrie viața grea a țăranilor din Câmpia Dunării în perioada interbelică. Prin ochii familiei Moromete, Preda aduce în prim-plan transformările sociale și impactul modernizării asupra vieții tradiționale rurale.', 101, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Harap-Alb', 'Ion Creangă', 'Povestea este un basm în care tânărul Harap-Alb trebuie să treacă prin mai multe încercări pentru a-și revendica moștenirea regală. Pe parcursul aventurii sale, el întâlnește personaje fabuloase și dobândește prieteni loiali. Este o operă care explorează temele curajului, prieteniei și destinului.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Moara cu noroc', 'Ioan Slavici', 'O nuvelă ce tratează destinul tragic al lui Ghiță, hangiul de la "Moara cu noroc", și al soției sale, Ana. Atracția pentru avere și dorința de ascensiune socială îl conduc pe Ghiță pe o cale întunecată. Povestea analizează temele moralității, a corupției și a avariei.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Enigma Otiliei', 'George Călinescu', 'Romanul prezintă viața Bucureștiului interbelic prin ochii tânărului Felix, care este fascinat de misterioasa Otilia. Relația lor este centrală operei, dar în jurul acesteia se dezvoltă o frescă a societății bucureștene, cu personaje memorabile și analiza psihologică.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Baltagul', 'Mihail Sadoveanu', 'Romanul descrie călătoria Vitoriei Lipan în căutarea soțului său, Nechifor Lipan, care a dispărut în munți. Este o explorare profundă a determinării și curajului unei femei, dar și o incursiune în credințele și superstițiile populare. "Baltagul" combina realismul cu elemente de mitologie populară.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Alexandru Lăpușneanu', 'Costache Negruzzi', 'O operă emblematică a romantismului românesc, ce relatează ascensiunea și căderea domnitorului moldovean Alexandru Lăpușneanu, punând accent pe conflictul dintre putere și moralitate.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Suflete tari', 'Camil Petrescu', 'Considerat un roman psihologic, "Suflete tari" este o analiză a complexității relațiilor umane, a caracterului iluzoriu al adevărului și a căutării identității în societatea interbelică.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Jocul ielelor', 'Camil Petrescu', 'O piesă de teatru ce se focusează pe introspecție și analiza subtilă a sentimentelor, reflectând teme precum dragostea, onoarea și efectele psihologice ale războiului.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Dramă')),
    ('Iona', 'Marin Sorescu', 'Dramă modernă ce reinterpretează povestea biblică a lui Iona, transformând-o într-o meditație despre condiția umană, izolare și căutarea sensului vieții.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Dramă')),
    ('Cel mai iubit dintre pământeni', 'Marin Preda', 'Roman postbelic profund, explorând tema libertății individuale în fața opresiunii și a alienării sociale prin povestea tragică a profesorului Victor Petrini.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Maitreyi', 'Mircea Eliade', 'Bazat pe propria experiență a autorului în India, romanul este o poveste de dragoste pasională, explorând contrastul între culturi și consecințele unui astfel de șoc cultural.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Patul lui Procust', 'Camil Petrescu', 'Un roman filozofic ce abordează ideea relativității adevărului și a percepției, prezentând conflictele interioare și exterioare ale protagonistului Fred Vasilescu.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Femeia în roșu', 'Adriana Babeți, Mircea Nedelciu, Mircea Mihăieș', 'Un roman postmodern ce urmărește narativ multiple perspective, oferind o viziune fragmentată asupra realității și a identității.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Zmeura de câmpie', 'Mircea Nedelciu', 'O operă narativă ce abordează teme precum realitatea comunistă românească, alienarea și căutarea autenticității personale într-un mediu represiv.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Epic')),
    ('Meșterul Manole', 'Lucian Blaga', 'Dramă simbolică ce se bazează pe legenda construirii Mănăstirii Argeșului, explorând teme precum sacrificiul artistic și conflictul între creație și distrugere.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Dramă'));

    
    -- Liric
INSERT INTO `lecture` (`title`, `author`, `description`, `chunks`, `id_category`) VALUES
    ('Luceafărul', 'Mihai Eminescu', 'Considerată capodopera lui Eminescu, "Luceafărul" reprezintă lupta dintre ideal și realitate. Prin relația dintre Hyperion și Cătălina, poezia discută dualitatea dintre spirit și materie, aspirație și destin.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Scrisoarea I', 'Mihai Eminescu', 'Reflectând asupra decadenței Romei antice, aceasta poezie explorează efemeritatea imperiilor și trăinicia timpului.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Scrisoarea III', 'Mihai Eminescu', 'Un omagiu adus lui Ștefan cel Mare, poezia combină patriotismul cu reflecții istorice și filozofice despre destinul național.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Dorință', 'Mihai Eminescu', 'Un vers al pasiunii și dorinței, aceasta poezie ilustrează intensitatea sentimentului amoros într-o atmosferă de seră.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Floare albastră', 'Mihai Eminescu', 'Evocând iubirea neîmplinită și aspirația spre ideal, poezia se folosește de simbolul floarei albastre pentru a exprima dorința arzătoare.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Mai am un singur dor', 'Mihai Eminescu', 'Exprimând tema sacrificiului și a dorinței de eliberare de suferință, poezia reflectă asupra efemerității și tristeții vieții.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Testament', 'Tudor Arghezi', 'O reflexie profundă asupra moștenirii spirituale, Arghezi consideră creația sa ca un dar pentru posteritate.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Flori de mucigai', 'Tudor Arghezi', 'Explorând ideea de frumusețe în decădere, poezia juxtapune imagini ale vieții și morții, subliniind ciclicitatea existenței.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Eu nu strivesc corola de minuni a lumii', 'Lucian Blaga', 'Poezia discută relația dintre om și misterul universului, subliniind respectul față de secretele existenței.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('În grădina Ghetsemani', 'Lucian Blaga', 'Evocând grădina biblică, poezia reflectă asupra sacrificiului și trăirilor intense în fața destinului.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('La tiganci', 'Lucian Blaga', 'Poezia ilustrează o lume de vis și mister, cu elemente suprarealiste și reflecții asupra realității și fanteziei.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Leoaică tânără, iubirea...', 'Nichita Stănescu', 'O celebrare a iubirii tinere și pasionale, poezia juxtapune imagini ale vitalității cu cele ale vulnerabilității.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Rugăciune', 'Octavian Goga', '"Rugăciune" de Octavian Goga este o poezie profundă în care poetul exprimă, în termeni emoționanți, aspirațiile naționale și suferința poporului său. Poezia combină fervoarea religioasă cu pasiunea patriotică, fiind un strigăt către divinitate pentru îndurare și ajutor în vremuri de cumpănă, oglindind astfel angajamentul lui Goga față de valorile naționale și dragostea sa față de țărănimea română.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Moartea lui Fulger', 'George Coșbuc', 'Poezia prezintă o alegorie a vitejiei și a sfârșitului tragic al eroului mitic Fulger, simbolizând lupta și caducitatea eroismului uman.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Malul Siretului', 'Vasile Alecsandri', 'Această operă lirică exprimă dragostea lui Alecsandri pentru peisajele românești, în special pentru malurile Siretului, prin descrieri evocative și sentimentale.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Plumb', 'George Bacovia', 'Poemul "Plumb" este emblematic pentru simbolismul românesc, transmițând stări de melancolie profundă și izolare prin imagini sumbre și dense.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Lacustră', 'George Bacovia', 'Poezia este expresia simbolistă a stărilor de melancolie și singurătate, evocând atmosfera apăsătoare a peisajelor lacustre sub cerul plumburiu.', 20, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric'));

    
    -- Dramă
INSERT INTO `lecture` (`title`, `author`, `description`, `chunks`, `id_category`) VALUES
    ('O scrisoare pierdută', 'I.L. Caragiale', 'Una dintre cele mai reprezentative opere ale lui Caragiale, "O scrisoare pierdută" este o satiră acută la adresa mediului politic românesc de la sfârșitul secolului XIX. Povestea gravitează în jurul unei scrisori compromițătoare pierdute de un politician, care devine obiectul unei goane frenetice. Prin umorul său inconfundabil, Caragiale evidențiază ipocrizia, corupția și oportunistismul care domină societatea. Caracterizarea precisă a personajelor și dialogul savuros transformă piesa într-o capodoperă a teatrului românesc, având o relevanță care depășește epoca sa.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Dramă')),
    ('Riga Crypto și lapona Enigel', 'Ion Barbu', 'Deși mai cunoscut ca poet, Ion Barbu a scris și această dramă simbolică, "Riga Crypto și lapona Enigel", care explorează tema identității și a contrastului dintre civilizație și natură. Piesa urmărește interacțiunea dintre două personaje centrale, Riga Crypto, un miner, și Lapona Enigel, reprezentând lumea naturală. Dialogul dintre ei aduce în discuție concepte filozofice și conflictele inerente diferențelor lor. Prin această dramă, Barbu oferă o meditație profundă asupra umanității, culturii și relației cu natura.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Dramă'));

    
    -- Populare
INSERT INTO `lecture` (`title`, `author`, `description`, `chunks`, `id_category`) VALUES

    ('Amintiri din copilărie', 'Ion Creangă', 'Considerată o capodoperă a literaturii române, "Amintiri din copilărie" reprezintă o autobiografie stilizată a lui Ion Creangă. Scriitorul își reînvie amintirile din copilărie, recreând atmosfera satului său natal și a perioadei de nevinovăție. Prin ochii micului Nică, cititorii sunt invitați într-o lume plină de culoare, umor și aventuri, unde natura, oamenii și obiceiurile capătă o strălucire aparte. Lucrarea este nu doar o colecție de amintiri personale, ci și un portret viu al vieții rurale din Moldova secolului XIX, prezentat cu sinceritate, căldură și o profundă dragoste pentru locurile natale.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Populare')),
    ('Ora Fântânilor', 'Ion Vinea', 'Opera "Ora Fântânilor" de Ion Vinea este o lucrare emblematică pentru literatura modernistă românească, renumită pentru stilul său inovativ și tehnicile narative avangardiste. Prin intermediul acestei opere, Vinea oferă o perspectivă unică asupra urbanismului și transformărilor sociale ale epocii interbelice. Textul, impregnat de simboluri și imagini poetice, explorează tema alienării în metropola în expansiune și reflectă căutarea individualității în fața modernizării accelerate. "Ora Fântânilor" rămâne o lucrare de referință pentru dinamica culturală a perioadei sale, fiind totodată o mărturie a evoluției poetice a autorului.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Aci sosi pe vremuri', 'Ion Pillat', 'Poemul "Aci sosi pe vremuri" de Ion Pillat este o meditație lirică asupra trecutului și a impactului său asupra prezentului. Prin limbajul său evocator și imagistica sa bogată, Pillat împletește peisajul natural cu cel cultural și istoric, reflectând asupra vestigiilor timpului pe pământul românesc. Versurile sale cuprind un sentiment profund de nostalgie și o reverență pentru moștenirea culturală, fiind o rememorare poetică a momentelor și figurilor semnificative din istoria românească. Este o piesă emblematică pentru lirismul interbelic și pentru capacitatea poeziei de a traversa timpul, punând în lumină legătura dintre natură, umanitate și istorie.', 1, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric'));


/*    ('Basme (alese)', 'Ion Creangă', 'O selecție de basme nemuritoare scrise de Ion Creangă, unul dintre cei mai iubiți autori români de povești populare. Basmele sale sunt povestite cu o savoare unică, îmbinând elemente tradiționale din folclorul românesc cu umorul, moralitatea și înțelepciunea specifică scriitorului. Prin personajele sale memorabile, precum Harap-Alb sau Fata babei și fata moșneagului, Creangă aduce la viață universul magic și învățăturile străvechi ale poveștilor populare românești, fascinând generații la rând.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Populare')),
    ('A douasprezecea noapte sau Cum vă place', 'William Shakespeare', 'Una dintre cele mai populare comedii ale lui Shakespeare, "A douasprezecea noapte" este o poveste despre iubire, identitate și echivoc. Povestea urmărește peripețiile gemenei Viola, care se deghizează în bărbat și se îndrăgostește de ducele Orsino, în timp ce este confundată cu fratele ei, Sebastian. Prin situații comice, echivocuri și caracterizări memorabile, Shakespeare explorează confuziile sentimentelor și absurditățile comportamentului uman. Piesa este celebră pentru umorul său sofisticat, pentru dialogurile sclipitoare și pentru reflecțiile asupra naturii iubirii și a identității.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Dramă')),
    ('Oedip rege', 'Sofocle', 'O capodoperă a tragediei antice grecești, "Oedip rege", scrisă de Sofocle, este povestea tragică a regelui Oedip și a descoperirii sale terifiante despre propria origine și destin. Încercând să evite o profeție care spune că își va ucide tatăl și se va căsători cu mama, Oedip devine, fără să-și dea seama, instrumentul propriei sale nenorociri. Piesa explorează temele destinului, a auto-cunoașterii și a pedepsei divine. Prin structura sa narativă tensionată și prin dezvoltarea personajului, Sofocle oferă o meditație asupra naturii umane și a limitelor cunoașterii umane.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Dramă')),
    ('Silentio', 'Tudor Arghezi', 'O meditație lirică asupra tăcerii și introspecției, aceasta poezie atinge adâncimi ale solitudinii și contemplării.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Cuvânt', 'Tudor Arghezi', 'Reflectând asupra puterii și semnificației cuvântului, Arghezi meditează asupra rolului esențial al limbajului în viața umană.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('O viziune a sentimentelor', 'Nichita Stănescu', 'O introspecție a emoțiilor umane, poezia este o explorare a sentimentelor și a profundităților sufletului.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Emoție de toamnă', 'Nichita Stănescu', 'Capturând esența melancoliei toamnei, poezia reflectă asupra trecerii timpului și a sentimentelor efemere.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric')),
    ('Viziunea viziunii', 'Nichita Stănescu', 'Explorând conceptul de percepție și realitate, poezia discută relația dintre individ și universul său interior și exterior.', 30, (SELECT `id` FROM `lecture_category` WHERE `name` = 'Liric'));
*/;