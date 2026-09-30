import re

def update_blog(filename, new_title, new_meta, new_date, new_body):
    with open('blog-social-confidence.html', 'r') as f:
        content = f.read()

    # Generic replace for title, description, and h1
    content = re.sub(r'<title>.*?</title>', f'<title>{new_title} | Joyful Hearing Blog</title>', content)
    content = re.sub(r'name="description"\s+content=".*?"', f'name="description" content="{new_meta}"', content)
    content = re.sub(r'"name":\s*".*?"', f'"name": "{new_title}"', content, count=1)
    content = re.sub(r'"description":\s*".*?"', f'"description": "{new_meta}"', content, count=1)
    
    # Replace date
    content = re.sub(r'June 27, 2026', new_date, content, flags=re.IGNORECASE)
    
    # Replace the h1 tag
    content = re.sub(r'<h1 class="font-display text-4xl md:text-5xl font-bold text-joy-ink mb-6 leading-tight">\s*.*?\s*</h1>', f'<h1 class="font-display text-4xl md:text-5xl font-bold text-joy-ink mb-6 leading-tight">{new_title}</h1>', content)
    
    # Replace body
    content = re.sub(r'               <!-- Featured Image -->.*?</div>\s*<!-- Author Box -->', new_body + '\n\n               <!-- Author Box -->', content, flags=re.DOTALL)

    with open(filename, 'w') as f:
        f.write(content)

# BLOG 37
body_37 = """               <!-- Featured Image -->
               <div class="mb-10 rounded-none overflow-hidden shadow-sm">
                  <img src="assets/images/blog_37_hearing_loss_depression_1.jpg" alt="Hearing Loss and Depression" class="w-full h-auto object-cover object-top">
               </div>

               <!-- Typography Body -->
               <div class="prose prose-lg prose-slate max-w-none text-slate-700 leading-loose prose-headings:font-display prose-headings:font-bold prose-headings:uppercase prose-headings:tracking-wide prose-a:text-joy-blue prose-img:rounded-none text-justify">
                 
<p class="first-letter:text-5xl first-letter:font-bold first-letter:text-joy-blue first-letter:mr-3 first-letter:float-left">
When a person loses their hearing gradually, those around them often describe the change as the person becoming quieter, more withdrawn, more irritable, less engaged. What looks like a personality shift is often something more clinical. The relationship between untreated hearing loss and depression is one of the most robust findings in audiological research, and it is almost entirely preventable.
</p>

<h2>How hearing loss creates the conditions for depression</h2>
<p>The pathway is not sudden. It moves through four predictable stages. First, communication becomes exhausting. Following conversations in noisy environments, on the phone, or in groups requires intense, constant effort. Listening fatigue accumulates. Second, social withdrawal begins. The effort of hearing starts to outweigh the reward of socialising. Restaurants are avoided. Family calls become shorter. Gatherings feel more stressful than enjoyable. Third, isolation deepens. As the person participates less, relationships thin. Family members stop repeating themselves. The person is quietly left out of conversations and decisions. Fourth, depression develops. Chronic loneliness, loss of identity as a communicator, helplessness and the sense of being a burden create the psychological conditions for clinical depression.</p>

<div class="my-8 rounded-none overflow-hidden shadow-sm">
    <img src="assets/images/blog_37_hearing_loss_depression_2.jpg" alt="Conditions for depression" class="w-full h-auto object-cover">
</div>

<h2>The research is unambiguous</h2>
<p>Adults with untreated hearing loss are twice as likely to develop depression as those with normal hearing. They report significantly higher rates of anxiety, loneliness and social isolation. The effect is strongest in adults between 50 and 70, precisely the demographic most likely to dismiss hearing loss as a normal part of ageing and delay seeking help.</p>

<div class="my-8 rounded-none overflow-hidden shadow-sm">
    <img src="assets/images/blog_37_hearing_loss_depression_3.jpg" alt="Research insights" class="w-full h-auto object-cover">
</div>

<h2>Recognising the combined signs</h2>
<p>The challenge is that the behavioural signs of hearing loss and depression overlap significantly. Withdrawal, reduced conversation, increased irritability, fatigue and loss of interest in social activities can all be attributed to either condition. Families often address the mood symptoms first, through counselling or medication, without recognising that an unaddressed hearing problem is driving the cycle.</p>

<div class="my-8 rounded-none overflow-hidden shadow-sm">
    <img src="assets/images/blog_37_hearing_loss_depression_4.jpg" alt="Recognizing signs" class="w-full h-auto object-cover">
</div>

<h2>What actually helps</h2>
<p>The most effective single intervention is treating the hearing loss. Clinical studies consistently show that hearing aid users report significantly lower depression scores within three months of fitting, with the greatest improvements in those who were most isolated before treatment. Modern hearing aids reduce the listening effort that drives fatigue and withdrawal, making social re-engagement less costly and more sustainable.</p>
<p>Family involvement is equally important. Reducing background noise during conversations, speaking clearly and at a moderate pace, and patience with repetition all reduce the daily stress that accumulates into low mood.</p>

<div class="my-8 rounded-none overflow-hidden shadow-sm">
    <img src="assets/images/blog_37_hearing_loss_depression_5.jpg" alt="What actually helps" class="w-full h-auto object-cover">
</div>

<p>At Joyful Hearing and Speech Clinic, Lucknow, we work with families as well as patients to ensure that hearing treatment addresses both the audiological and the emotional dimensions of hearing loss.</p>

<div class="mt-8 p-6 bg-joy-blue/5 border border-joy-blue/20 rounded-none text-center">
    <h4 class="font-display font-bold text-joy-ink uppercase tracking-wider mb-2">Book Your Consultation</h4>
    <p class="text-sm text-slate-600 mb-4">Start your journey to better hearing and a more connected life.</p>
    <div class="flex flex-wrap justify-center gap-4">
        <a href="tel:+918240516775" class="bg-joy-blue text-white px-6 py-2 text-xs font-bold uppercase tracking-wider hover:bg-joy-blue/90 transition-colors">Call Clinic</a>
        <a href="https://wa.me/918240516775?text=Hi%2C%20I%27d%20like%20to%20book%20a%20consultation." target="_blank" rel="noreferrer" class="border border-[#2caa6a] text-[#187d4b] px-6 py-2 text-xs font-bold uppercase tracking-wider hover:bg-[#18964f] hover:text-white transition-colors">WhatsApp Us</a>
    </div>
</div>
               </div>"""


# BLOG 38
body_38 = """               <!-- Featured Image -->
               <div class="mb-10 rounded-none overflow-hidden shadow-sm">
                  <img src="assets/images/blog_38_presbycusis_1.jpg" alt="Presbycusis: Age-Related Hearing Loss" class="w-full h-auto object-cover object-top">
               </div>

               <!-- Typography Body -->
               <div class="prose prose-lg prose-slate max-w-none text-slate-700 leading-loose prose-headings:font-display prose-headings:font-bold prose-headings:uppercase prose-headings:tracking-wide prose-a:text-joy-blue prose-img:rounded-none text-justify">
                 
<p class="first-letter:text-5xl first-letter:font-bold first-letter:text-joy-blue first-letter:mr-3 first-letter:float-left">
There is a word most people have never heard that describes something affecting one in three adults over the age of 60. Presbycusis is the medical term for age-related hearing loss. It is the gradual, progressive deterioration of hearing that occurs as the cochlea's sensory hair cells wear out after decades of use. It is painless, invisible, almost always affects both ears equally, and is among the most undertreated conditions in India.
</p>

<h2>What actually happens inside the ear</h2>
<p>The cochlea contains thousands of tiny hair cells arranged by frequency. The cells responsible for detecting high-frequency sounds sit at the base of the cochlea and are the first to be exposed to every sound entering the ear across a lifetime. They are also the first to wear out. This is why the earliest symptom of presbycusis is almost always difficulty hearing high-pitched consonants like S, F, TH and SH - the sounds that carry the most speech intelligibility. A person with early presbycusis hears the volume of speech but loses the clarity. They hear someone talking but cannot make out the words.</p>

<div class="my-8 rounded-none overflow-hidden shadow-sm">
    <img src="assets/images/blog_38_presbycusis_2.jpg" alt="What happens inside the ear" class="w-full h-auto object-cover">
</div>

<h2>The progression</h2>
<p>Presbycusis moves through broadly three stages. In the mild stage, most one-to-one conversation is manageable but noise becomes a significant challenge. Restaurants, family gatherings and group conversations start to feel effortful. In the moderate stage, repetition becomes a constant need, television volume creates household friction, and phone calls become genuinely difficult. In the severe stage, most speech is unclear even at close range without amplification, and social withdrawal often follows.</p>

<div class="my-8 rounded-none overflow-hidden shadow-sm">
    <img src="assets/images/blog_38_presbycusis_3.jpg" alt="The progression of presbycusis" class="w-full h-auto object-cover">
</div>

<h2>The numbers every family should know</h2>
<p>One in three adults over 60 has presbycusis. By 75, that figure rises to one in two. The average time between when hearing loss begins and when a person seeks help is ten years. During those ten years, the brain receives progressively less auditory input and begins to reassign the neural pathways that once processed sound. This reorganisation makes later rehabilitation harder and is strongly associated with accelerated cognitive decline.</p>

<div class="my-8 rounded-none overflow-hidden shadow-sm">
    <img src="assets/images/blog_38_presbycusis_4.jpg" alt="The numbers to know" class="w-full h-auto object-cover">
</div>

<h2>What to do</h2>
<p>A comprehensive audiogram is the starting point. It maps the specific frequencies affected and establishes a baseline for monitoring progression. Modern hearing aids, programmed precisely to the individual audiogram, are small, rechargeable and highly effective for presbycusis. Annual reassessments ensure devices remain calibrated to current hearing levels. Equally important is protecting the hearing that remains - presbycusis accelerates with noise exposure, and diabetics and smokers are at significantly elevated risk.</p>

<div class="my-8 rounded-none overflow-hidden shadow-sm">
    <img src="assets/images/blog_38_presbycusis_5.jpg" alt="What to do about presbycusis" class="w-full h-auto object-cover">
</div>

<p>At Joyful Hearing and Speech Clinic, Lucknow, we offer full audiological assessments, hearing aid trials and annual review programmes for patients with age-related hearing loss.</p>

<div class="mt-8 p-6 bg-joy-blue/5 border border-joy-blue/20 rounded-none text-center">
    <h4 class="font-display font-bold text-joy-ink uppercase tracking-wider mb-2">Book Your Consultation</h4>
    <p class="text-sm text-slate-600 mb-4">Start your journey to better hearing today.</p>
    <div class="flex flex-wrap justify-center gap-4">
        <a href="tel:+918240516775" class="bg-joy-blue text-white px-6 py-2 text-xs font-bold uppercase tracking-wider hover:bg-joy-blue/90 transition-colors">Call Clinic</a>
        <a href="https://wa.me/918240516775?text=Hi%2C%20I%27d%20like%20to%20book%20a%20consultation." target="_blank" rel="noreferrer" class="border border-[#2caa6a] text-[#187d4b] px-6 py-2 text-xs font-bold uppercase tracking-wider hover:bg-[#18964f] hover:text-white transition-colors">WhatsApp Us</a>
    </div>
</div>
               </div>"""


update_blog('blog-hearing-loss-depression.html', "Hearing Loss and Depression: The Silent Link Nobody Talks About", "Untreated hearing loss is strongly linked to depression. Learn how hearing aids can help you reconnect with the world and improve mental health.", "SEPTEMBER 29, 2026", body_37)
update_blog('blog-presbycusis.html', "Presbycusis: Understanding Age-Related Hearing Loss and What to Do About It", "Presbycusis affects one in three adults over 60. Learn about age-related hearing loss, its symptoms, and the best ways to treat it.", "SEPTEMBER 29, 2026", body_38)
