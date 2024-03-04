from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from django.conf import settings
import joblib as jb


# loading trained_model

model_path = os.path.join(settings.MEDIA_ROOT, "trained_model")
model = jb.load(model_path)


def home(request):
    if request.method == "GET":
        return JsonResponse({"message": "This just home page"})


@csrf_exempt
def predictDisease(request):
    if request.metho == "POST":
        diseaselist = [
            "Fungal infection",
            "Allergy",
            "GERD",
            "Chronic cholestasis",
            "Drug Reaction",
            "Peptic ulcer diseae",
            "AIDS",
            "Diabetes ",
            "Gastroenteritis",
            "Bronchial Asthma",
            "Hypertension ",
            "Migraine",
            "Cervical spondylosis",
            "Paralysis (brain hemorrhage)",
            "Jaundice",
            "Malaria",
            "Chicken pox",
            "Dengue",
            "Typhoid",
            "hepatitis A",
            "Hepatitis B",
            "Hepatitis C",
            "Hepatitis D",
            "Hepatitis E",
            "Alcoholic hepatitis",
            "Tuberculosis",
            "Common Cold",
            "Pneumonia",
            "Dimorphic hemmorhoids(piles)",
            "Heart attack",
            "Varicose veins",
            "Hypothyroidism",
            "Hyperthyroidism",
            "Hypoglycemia",
            "Osteoarthristis",
            "Arthritis",
            "(vertigo) Paroymsal  Positional Vertigo",
            "Acne",
            "Urinary tract infection",
            "Psoriasis",
            "Impetigo",
        ]

        symptomslist = [
            "itching",
            "skin_rash",
            "nodal_skin_eruptions",
            "continuous_sneezing",
            "shivering",
            "chills",
            "joint_pain",
            "stomach_pain",
            "acidity",
            "ulcers_on_tongue",
            "muscle_wasting",
            "vomiting",
            "burning_micturition",
            "spotting_ urination",
            "fatigue",
            "weight_gain",
            "anxiety",
            "cold_hands_and_feets",
            "mood_swings",
            "weight_loss",
            "restlessness",
            "lethargy",
            "patches_in_throat",
            "irregular_sugar_level",
            "cough",
            "high_fever",
            "sunken_eyes",
            "breathlessness",
            "sweating",
            "dehydration",
            "indigestion",
            "headache",
            "yellowish_skin",
            "dark_urine",
            "nausea",
            "loss_of_appetite",
            "pain_behind_the_eyes",
            "back_pain",
            "constipation",
            "abdominal_pain",
            "diarrhoea",
            "mild_fever",
            "yellow_urine",
            "yellowing_of_eyes",
            "acute_liver_failure",
            "fluid_overload",
            "swelling_of_stomach",
            "swelled_lymph_nodes",
            "malaise",
            "blurred_and_distorted_vision",
            "phlegm",
            "throat_irritation",
            "redness_of_eyes",
            "sinus_pressure",
            "runny_nose",
            "congestion",
            "chest_pain",
            "weakness_in_limbs",
            "fast_heart_rate",
            "pain_during_bowel_movements",
            "pain_in_anal_region",
            "bloody_stool",
            "irritation_in_anus",
            "neck_pain",
            "dizziness",
            "cramps",
            "bruising",
            "obesity",
            "swollen_legs",
            "swollen_blood_vessels",
            "puffy_face_and_eyes",
            "enlarged_thyroid",
            "brittle_nails",
            "swollen_extremeties",
            "excessive_hunger",
            "extra_marital_contacts",
            "drying_and_tingling_lips",
            "slurred_speech",
            "knee_pain",
            "hip_joint_pain",
            "muscle_weakness",
            "stiff_neck",
            "swelling_joints",
            "movement_stiffness",
            "spinning_movements",
            "loss_of_balance",
            "unsteadiness",
            "weakness_of_one_body_side",
            "loss_of_smell",
            "bladder_discomfort",
            "foul_smell_of urine",
            "continuous_feel_of_urine",
            "passage_of_gases",
            "internal_itching",
            "toxic_look_(typhos)",
            "depression",
            "irritability",
            "muscle_pain",
            "altered_sensorium",
            "red_spots_over_body",
            "belly_pain",
            "abnormal_menstruation",
            "dischromic _patches",
            "watering_from_eyes",
            "increased_appetite",
            "polyuria",
            "family_history",
            "mucoid_sputum",
            "rusty_sputum",
            "lack_of_concentration",
            "visual_disturbances",
            "receiving_blood_transfusion",
            "receiving_unsterile_injections",
            "coma",
            "stomach_bleeding",
            "distention_of_abdomen",
            "history_of_alcohol_consumption",
            "fluid_overload",
            "blood_in_sputum",
            "prominent_veins_on_calf",
            "palpitations",
            "painful_walking",
            "pus_filled_pimples",
            "blackheads",
            "scurring",
            "skin_peeling",
            "silver_like_dusting",
            "small_dents_in_nails",
            "inflammatory_nails",
            "blister",
            "red_sore_around_nose",
            "yellow_crust_ooze",
        ]

        psymptomsList = json.loads(request.POST["symptoms"])
        psymptoms = [symptom["value"] for symptom in psymptomsList]
        if len(psymptoms) > 7:
            return JsonResponse(
                {
                    "message": "symptoms exceeded the number limit",
                    "predicteddisease": "None",
                    "confidencescore": 0,
                    "consultdoctor": "None",
                }
            )
        if not psymptoms:
            return JsonResponse(
                {
                    "predicteddisease": "None",
                    "confidencescore": 0,
                    "consultdoctor": "None",
                }
            )

        testingsymptoms = []
        # append zero in all coloumn fields...
        for x in range(0, len(symptomslist)):
            testingsymptoms.append(0)

        # update 1 where symptoms gets matched...
        for k in range(0, len(symptomslist)):
            for z in psymptoms:
                if z == symptomslist[k]:
                    testingsymptoms[k] = 1

        inputtest = [testingsymptoms]

        predicted = model.predict(inputtest)
        # print("predicted disease is : ")
        # print(predicted)
        y_pred_2 = model.predict_proba(inputtest)
        confidencescore = y_pred_2.max() * 100

        predicted_disease = predicted[0]

        """
        doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
                                    "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]
        """

        Rheumatologist = ["Osteoarthristis", "Arthritis"]

        Cardiologist = ["Heart attack", "Bronchial Asthma", "Hypertension "]

        ENT_specialist = ["(vertigo) Paroymsal  Positional Vertigo", "Hypothyroidism"]

        Orthopedist = []

        Neurologist = [
            "Varicose veins",
            "Paralysis (brain hemorrhage)",
            "Migraine",
            "Cervical spondylosis",
        ]

        Allergist_Immunologist = [
            "Allergy",
            "Pneumonia",
            "AIDS",
            "Common Cold",
            "Tuberculosis",
            "Malaria",
            "Dengue",
            "Typhoid",
        ]

        Urologist = ["Urinary tract infection", "Dimorphic hemmorhoids(piles)"]

        Dermatologist = [
            "Acne",
            "Chicken pox",
            "Fungal infection",
            "Psoriasis",
            "Impetigo",
        ]

        Gastroenterologist = [
            "Peptic ulcer diseae",
            "GERD",
            "Chronic cholestasis",
            "Drug Reaction",
            "Gastroenteritis",
            "Hepatitis E",
            "Alcoholic hepatitis",
            "Jaundice",
            "hepatitis A",
            "Hepatitis B",
            "Hepatitis C",
            "Hepatitis D",
            "Diabetes ",
            "Hypoglycemia",
        ]

        if predicted_disease in Rheumatologist:
            consultdoctor = "Rheumatologist"

        if predicted_disease in Cardiologist:
            consultdoctor = "Cardiologist"

        elif predicted_disease in ENT_specialist:
            consultdoctor = "ENT specialist"

        elif predicted_disease in Orthopedist:
            consultdoctor = "Orthopedist"

        elif predicted_disease in Neurologist:
            consultdoctor = "Neurologist"

        elif predicted_disease in Allergist_Immunologist:
            consultdoctor = "Allergist/Immunologist"

        elif predicted_disease in Urologist:
            consultdoctor = "Urologist"

        elif predicted_disease in Dermatologist:
            consultdoctor = "Dermatologist"

        elif predicted_disease in Gastroenterologist:
            consultdoctor = "Gastroenterologist"

        else:
            consultdoctor = "other"

        response = {
            "predicteddisease": predicted_disease,
            "confidencescore": confidencescore,
            "consultdoctor": consultdoctor,
        }
        print("RESPONSE------------------------\n", response)
        return JsonResponse(response)
    else:
        return JsonResponse(
            {"method": request.method, "message": "Post method is required!!"}
        )
