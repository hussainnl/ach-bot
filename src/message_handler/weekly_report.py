from databases.mongodb.ach_report import AchReport as AR

def prepare_weekly_report(user_id,group_id):
    """To prepare the user weekly report"""
    raw_report = AR().get_user_raw_report(user_id,group_id)
    group_name = f"تقريرك الأسبوعي في جروب {raw_report['group_name']}:"
    user_score =f"عدد نقاط  :{raw_report['user_score']}"
    study_ach_list = raw_report['study_ach']
    weekly_ach = raw_report['weekly_ach']
    study_achs = f"الإنجازات الدراسي :\n{prepare_study_achs(study_ach_list)}"
    weekly_report = f"""{group_name}\n{user_score}\n{study_achs}\n{weekly_ach}
    """
    return weekly_report

def prepare_study_achs(study_ach_list):
    """To prepare the user study achievements in a good format"""
    ach_num = 0
    achs_study = ""
    for study_ach in study_ach_list :
        ach_num = ach_num +1
        achs_study =  achs_study + f"{ach_num}.{study_ach}  \n"
    return achs_study