import h2o


def map_Gender(Gender):
    return {'Male': 0, 'Female': 1}.get(Gender)


def map_MariStat(MariStat):
    return {'Other': 0, 'Alone': 1}.get(MariStat)


def map_yes_no(answ):
    return {'No': 0, 'Yes': 1}.get(answ)


def f_VehUsage(vu):
    vu_tuple = (
        int(vu == 'Professional'),
        int(vu == 'Private+trip to office'),
        int(vu == 'Private'),
        int(vu == 'Professional run')
    )
    return vu_tuple


def f_SocioCateg(sc):
    sc_list = [0, ]*7
    ind = int(sc[-1])
    sc_list[ind-1] = 1
    return tuple(sc_list)


def return_NewH2o_Frame():
    columns = [
        'Exposure',
        'LicAge',
        'Gender',
        'MariStat',
        'DrivAge',
        'DrivAgeSq',

        'HasKmLimit',
        'BonusMalus',
        'OutUseNb',
        'RiskArea',

        'VehUsage_Private',
        'VehUsage_Private + trip to office',
        'VehUsage_Professional',
        'VehUsage_Professional run',

        'SocioCateg_CSP1',
        'SocioCateg_CSP2',
        'SocioCateg_CSP3',
        'SocioCateg_CSP4',
        'SocioCateg_CSP5',
        'SocioCateg_CSP6',
        'SocioCateg_CSP7'
    ]
    return h2o.H2OFrame([[0, ] * 21], column_names=columns)


def process_input(json_input):
    Exposure = json_input["Exposure"]
    LicAge = json_input["LicAge"]
    Gender = map_Gender(json_input["Gender"])
    MariStat = map_MariStat(json_input["MariStat"])
    DrivAge = json_input["DrivAge"]
    DrivAgeSq = DrivAge ** 2

    HasKmLimit = map_yes_no(json_input["HasKmLimit"])
    BonusMalus = json_input["BonusMalus"]
    OutUseNb = json_input["OutUseNb"]
    RiskArea = json_input["RiskArea"]

    VehUsg = f_VehUsage(json_input["VehUsage"])
    VehUsg_Private = VehUsg[0]
    VehUsg_Private_trip_to_office = VehUsg[1]
    VehUsg_Professional = VehUsg[2]
    VehUsg_Professional_run = VehUsg[3]

    SocioCateg = f_SocioCateg(json_input["SocioCateg"])
    SocioCateg_CSP1 = SocioCateg[0]
    SocioCateg_CSP2 = SocioCateg[1]
    SocioCateg_CSP3 = SocioCateg[2]
    SocioCateg_CSP4 = SocioCateg[3]
    SocioCateg_CSP5 = SocioCateg[4]
    SocioCateg_CSP6 = SocioCateg[5]
    SocioCateg_CSP7 = SocioCateg[6]

    hf = return_NewH2o_Frame()

    hf[0, 'Exposure'] = Exposure
    hf[0, 'LicAge'] = LicAge
    hf[0, 'Gender'] = Gender
    hf[0, 'MariStat'] = MariStat
    hf[0, 'DrivAge'] = DrivAge
    hf[0, 'DrivAgeSq'] = DrivAgeSq

    hf[0, 'HasKmLimit'] = HasKmLimit
    hf[0, 'BonusMalus'] = BonusMalus
    hf[0, 'OutUseNb'] = OutUseNb
    hf[0, 'RiskArea'] = RiskArea

    hf[0, 'VehUsg_Private'] = VehUsg_Private
    hf[0, 'VehUsg_Private+trip to office'] = VehUsg_Private_trip_to_office
    hf[0, 'VehUsg_Professional'] = VehUsg_Professional
    hf[0, 'VehUsg_Professional run'] = VehUsg_Professional_run

    hf[0, 'CSP1'] = SocioCateg_CSP1
    hf[0, 'CSP2'] = SocioCateg_CSP2
    hf[0, 'CSP3'] = SocioCateg_CSP3
    hf[0, 'CSP3'] = SocioCateg_CSP4
    hf[0, 'CSP3'] = SocioCateg_CSP5
    hf[0, 'CSP6'] = SocioCateg_CSP6
    hf[0, 'CSP7'] = SocioCateg_CSP7

    return hf
