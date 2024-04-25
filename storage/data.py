# /storage/data.py

avatar_data = [
    {"title": "Boy1", "description": "Description for Avatar 1", "image": "/assets/avatars/boy1.png", "is_active": True},
    {"title": "Boy2", "description": "Description for Avatar 2", "image": "/assets/avatars/boy2.png", "is_active": True},
    {"title": "Boy3", "description": "Description for Avatar 3", "image": "/assets/avatars/boy3.png", "is_active": True},
    {"title": "Girl1", "description": "Description for Avatar 4", "image": "/assets/avatars/girl1.png", "is_active": True},
    {"title": "Girl2", "description": "Description for Avatar 5", "image": "/assets/avatars/girl2.png", "is_active": True},
    {"title": "Girl3", "description": "Description for Avatar 6", "image": "/assets/avatars/girl3.png", "is_active": True}
]

user_data = [
    {"avatar_id": 1, "username": "Hassan", "description": "Description for User1", "age": 8, "password": "Hassan123", "exp_points": 0, "is_active": True},
    {"avatar_id": 2, "username": "Naashit", "description": "Description for User2", "age": 9, "password": "Naashit123", "exp_points": 0, "is_active": True},
    {"avatar_id": 1, "username": "Saim", "description": "Description for User3", "age": 11, "password": "Saim123", "exp_points": 0, "is_active": True},
    {"avatar_id": 2, "username": "Sameer", "description": "Description for User4", "age": 10, "password": "Sameer123", "exp_points": 0, "is_active": True}
]

quiz_data = [
    {"title": "Namaz", "description": "Namaz Description", "is_active": True},
    {"title": "Quran", "description": "Quran Description", "is_active": True},
    {"title": "Hadith", "description": "Hadith Description", "is_active": True},
    {"title": "Dua", "description": "Dua Description", "is_active": True},
    {"title": "Noorani Qaida", "description": "Noorani Qaida Description", "is_active": True}
]

quiz_level_data = [
    {"quiz_id": 1, "title": "Namaz Level 1", "description": "Description for Quiz Level 1", "no_of_questions": 10, "is_active": True},
    {"quiz_id": 1, "title": "Namaz Level 2", "description": "Description for Quiz Level 2", "no_of_questions": 0, "is_active": True},
    {"quiz_id": 1, "title": "Namaz Level 3", "description": "Description for Quiz Level 3", "no_of_questions": 0, "is_active": True}
]

# Question Types
# TextImage
# TextArabic
# TextAudio
# TextImageArabic
# TextImageAudio

# Answer Types
# Text
# Image
# Audio

quiz_question_data = [
    {"quiz_level_id": 1, "title": "Question 1", "description": "Description for Question 1", "age_group": "7-9",
     "question_type": "TextImage", "question_text": "What is the arabic word for prayers?", "arabic_text": None, "arabic_text_audio": None, "question_image": "https://drive.google.com/file/d/1I8ztmJhmG1AqcxFRBBXaLmohfzPlu-HB/view?usp=drive_link", "question_audio": None, "question_video": None,
     "answer_type": "Text", "correct_option": "option1", "option1": "Salah", "option2": "Hajj", "option3": "Bismillah", "option4": "Ruku", 
     "is_active": True},

    {"quiz_level_id": 1, "title": "Question 2", "description": "Description for Question 2", "age_group": "7-9",
     "question_type": "TextImage", "question_text": "what verse we recite in sajda during namaz?", "arabic_text": None, "arabic_text_audio": None, "question_image": "https://drive.google.com/file/d/1cPGmso6kE3UhBFm5yWG1CVsBhWCaolfQ/view?usp=drive_link", "question_audio": None, "question_video": None,
     "answer_type": "Audio", "correct_option": "option2", "option1": "https://drive.google.com/file/d/1UEu2mzSiSMcExIfKMeM8u2cGBV1-KZhv/view?usp=drive_link", "option2": "https://drive.google.com/file/d/1ckuvK5Xb1Z81n4VrEz3VUOwkpqrOhBQC/view?usp=drive_link", "option3": "https://drive.google.com/file/d/1tE7ndRg0n9_xuwZwCpTefAej0H612P60/view?usp=drive_link", "option4": "https://drive.google.com/file/d/1loqRaWcq1sV0VeF3_Cm7wo3TBNuuVIUh/view?usp=drive_link", 
     "is_active": True},

    {"quiz_level_id": 1, "title": "Question 3", "description": "Description for Question 3", "age_group": "7-9",
     "question_type": "TextAudio", "question_text": "what is the following verse is called in salah?", "arabic_text": "الله أكبرى", "arabic_text_audio": "https://drive.google.com/file/d/13u_OALiozjAhwrRfecWft3Owr-l3SB10/view?usp=drive_link", "question_image": None, "question_audio": None, "question_video": None,
     "answer_type": "Text", "correct_option": "option1", "option1": "takbeer-e-tahrema", "option2": "salaam", "option3": "fast", "option4": "takbeer", 
     "is_active": True},

    {"quiz_level_id": 1, "title": "Question 4", "description": "Description for Question 4", "age_group": "7-9",
     "question_type": "TextAudio", "question_text": "match the following voice with the correct option ", "arabic_text": "سُبْحَانَ رَبِّيَ الْعَظِيمِ", "arabic_text_audio": "https://drive.google.com/file/d/1Ej2D5pFlXJTwpDNzr3vrHU9CgPm0empD/view?usp=drive_link", "question_image": None, "question_audio": None, "question_video": None,
     "answer_type": "Audio", "correct_option": "option4", "option1": "https://drive.google.com/file/d/196DhXJYfy-8jjpNN4lSZkxhSOtNOvSDD/view?usp=drive_link", "option2": "https://drive.google.com/file/d/1r8gIbyGV8J_MkG2JfJSQH7tZKR_sYbzr/view?usp=drive_link", "option3": "https://drive.google.com/file/d/1mrVK2DdaTKYXTLrHmJ29p3uD2RxFaN_u/view?usp=drive_link", "option4": "https://drive.google.com/file/d/1ZZTSBIO4HHAP9Mj0V4_YMx9C_i0TfxoT/view?usp=drive_link", 
     "is_active": True},

    {"quiz_level_id": 1, "title": "Question 5", "description": "Description for Question 5", "age_group": "7-9",
     "question_type": "TextAudio", "question_text": "match the following voice with the correct option", "arabic_text": "سُبْحَانَ رَبِّيَ الأَعْلَى", "arabic_text_audio": "https://drive.google.com/file/d/1xFBHI3F0-XaRd9_i940dVY3VyARfTaXf/view?usp=drive_link", "question_image": None, "question_audio": None, "question_video": None,
     "answer_type": "Audio", "correct_option": "option4", "option1": "https://drive.google.com/file/d/1QsC7hwMB60Aot9QPQwQ5H9AojsMXK1AF/view?usp=drive_link", "option2": "https://drive.google.com/file/d/1r4z70Hai2fQIpYfMYz0wYKCFf6SkqSpq/view?usp=drive_link", "option3": "https://drive.google.com/file/d/1x9_6GDfsswO5JxAmT096xk6NzeDHwNey/view?usp=drive_link", "option4": "https://drive.google.com/file/d/1nMvQbfdiaM1q3d_9a8AKj7Q1BIoZUSpz/view?usp=drive_link", 
     "is_active": True},

    {"quiz_level_id": 1, "title": "Question 6", "description": "Description for Question 6", "age_group": "10-12",
     "question_type": "TextAudio", "question_text": "in which part of namaz we recite the following verse", "arabic_text": "سُبْحَانَ رَبِّيَ الأَعْلَى", "arabic_text_audio": "https://drive.google.com/file/d/1xqeuStsi3rAe3Vh72wIFfVZ3iLFXgEuM/view?usp=drive_link", "question_image": None, "question_audio": None, "question_video": None,
     "answer_type": "Text", "correct_option": "option4", "option1": "Ruku", "option2": "Qayaam", "option3": "Salaam", "option4": "Sajda", 
     "is_active": True},
    
    {"quiz_level_id": 1, "title": "Question 7", "description": "Description for Question 1", "age_group": "10-12",
     "question_type": "TextAudio", "question_text": "where the follwing verse is recited in namaz", "arabic_text": "السلام عليكم ورحمة الله", "arabic_text_audio": "https://drive.google.com/file/d/1jvZw1jP5olJqUV2WJxyS9FO8eOTypJwR/view?usp=drive_link", "question_image": None, "question_audio": None, "question_video": None,
     "answer_type": "Text", "correct_option": "option3", "option1": "after namaz", "option2": "before namaz", "option3": "To end namaz", "option4": "mid of namaz", 
     "is_active": True},

    {"quiz_level_id": 1, "title": "Question 8", "description": "Description for Question 7", "age_group": "10-12",
     "question_type": "TextImage", "question_text": "How many sajood are there in one rakah", "arabic_text": "", "arabic_text_audio": None, "question_image": "https://drive.google.com/file/d/1GNbXhBDgESPzIHdozzgpFI0m-wb9D0iL/view?usp=drive_link", "question_audio": None, "question_video": None,
     "answer_type": "Text", "correct_option": "option2", "option1": "1", "option2": "2", "option3": "3", "option4": "4", 
     "is_active": True},

     {"quiz_level_id": 1, "title": "Question 9", "description": "Description for Question 7", "age_group": "10-12",
     "question_type": "TextImage", "question_text": "How many ruku's are there in one rakah", "arabic_text": "", "arabic_text_audio": None, "question_image": "https://drive.google.com/file/d/1VsntZOg-NtMPVUh87-dlMhi-9I4i12lL/view?usp=drive_link", "question_audio": None, "question_video": None,
     "answer_type": "Text", "correct_option": "option2", "option1": "1", "option2": "2", "option3": "3", "option4": "4", 
     "is_active": True},

    {"quiz_level_id": 1, "title": "Question 10", "description": "Description for Question 1", "age_group": "10-12",
     "question_type": "TextImage", "question_text": "Is Wudhu is must for offering namaz", "arabic_text": None, "arabic_text_audio": None, "question_image": "https://drive.google.com/file/d/1QnxFzWOdRIhlDBMnBAjDsACvvO511JA-/view?usp=drive_link", "question_audio": None, "question_video": None,
     "answer_type": "Text", "correct_option": "option1", "option1": "Yes", "option2": "No", "option3": "not really", "option4": "not at all", 
     "is_active": True},
]

users_quiz_levels_result_data = [
    {"quiz_level_id": 1, "user_id": 1, "status": "Completed"},
    {"quiz_level_id": 1, "user_id": 2, "status": "Completed"},
    {"quiz_level_id": 1, "user_id": 3, "status": "Unlocked"},
    {"quiz_level_id": 1, "user_id": 4, "status": "Unlocked"}
]

lesson_data = [
    {"title": "Namaz", "description": "Namaz Description", "is_active": True},
    {"title": "Quran", "description": "Quran Description", "is_active": True},
    {"title": "Hadith", "description": "Hadith Description", "is_active": True},
    {"title": "Dua", "description": "Dua Description", "is_active": True},
    {"title": "Noorani Qaida", "description": "Noorani Qaida Description", "is_active": True}
]

lesson_level_data = [
    {"lesson_id": 5, "title": "Takhti 15", "description": "Description for Takhti 15", "no_of_questions": 2, "is_active": True},
    {"lesson_id": 5, "title": "Takhti 16", "description": "Description for Takhti 16", "no_of_questions": 3, "is_active": True}
]

lesson_question_data = [
    {"lesson_level_id": 1, "title": "Takhti 15 part 1", "description": "Description for Takhti 15 part 1", "age_group": "7-9",
     "question_type": "TextAudio", "question_text": "Listen and study the following Takhti", "arabic_text": "یَزَّکَّی یَذَّکَّرُ اَلٌمُدَّثِرُ اَلٌمُزَّمِّلُ عِلِّیِّیٗنَ عِلِّیُّوٗنَ", "arabic_text_audio": "https://drive.google.com/file/d/1x6U_yptf_oFgtyLallD6YozshUZVw26J/view?usp=drive_link", "question_image": None, "question_audio": None, "question_video": None,
     "is_active": True},

    {"lesson_level_id": 1, "title": "Takhti 15 part 2", "description": "Description for Takhti 15 part 2", "age_group": "7-9",
     "question_type": "TextAudio", "question_text": "Listen and study the following Takhti", "arabic_text": "اِنَّ الَّذِیٗنَ الَّاالَّذِیٗنَ مِنٗ شَرِّ النَّفَّثٰتِ فَعَالُ لِّمَایُرِیٗرُ", "arabic_text_audio": "https://drive.google.com/file/d/1-qAPiLOwg5lopqX-1m2ucV_4sykmFQkU/view?usp=drive_link", "question_image": None, "question_audio": None, "question_video": None,
     "is_active": True},
    
    {"lesson_level_id": 2, "title": "Takhti 16 part 1", "description": "Description for Takhti 16 part 1", "age_group": "7-9",
     "question_type": "TextAudio", "question_text": "Listen and study the following Takhti", "arabic_text": "ضَالًا دَابَةٍ حَاجَكَ حَاجُوكَ لَضَالُونَ", "arabic_text_audio": "https://drive.google.com/file/d/1NFQnNpLb9ARpPDidqdWWx_-yrDJS3y3L/view?usp=drive_link", "question_image": None, "question_audio": None, "question_video": None,
     "is_active": True},
     
    {"lesson_level_id": 2, "title": "Takhti 16 part 2", "description": "Description for Takhti 16 part 2", "age_group": "7-9",
     "question_type": "TextAudio", "question_text": "Listen and study the following Takhti", "arabic_text": "وَلَا الضَّالِينَ اتحاجونى ولا تحضُونَ وَالصَّفت جَاءَتِ الصَّاخَةُ", "arabic_text_audio": "https://drive.google.com/file/d/1p8irjqCxU45h5lDVAIRjHzHUcpawlmXe/view?usp=drive_link", "question_image": None, "question_audio": None, "question_video": None,
     "is_active": True},

    {"lesson_level_id": 2, "title": "Takhti 16 part 3", "description": "Description for Takhti 16 part 3", "age_group": "7-9",
     "question_type": "TextAudio", "question_text": "Listen and study the following Takhti", "arabic_text": "فَإِذَا جَاءَتِ الظَّامَةُ الكبرى. صَوَافَ", "arabic_text_audio": "https://drive.google.com/file/d/15Dp90v4J_YzyRSzvJLWeBDrMFwYfM7R8/view?usp=drive_link", "question_image": None, "question_audio": None, "question_video": None,
     "is_active": True}
]

users_lesson_levels_result_data = [
    {"lesson_level_id": 1, "user_id": 1, "status": "Completed"},
    {"lesson_level_id": 1, "user_id": 2, "status": "Completed"},
    {"lesson_level_id": 1, "user_id": 3, "status": "Unlocked"},
    {"lesson_level_id": 1, "user_id": 4, "status": "Unlocked"}
]
