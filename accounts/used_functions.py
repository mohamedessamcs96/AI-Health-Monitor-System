def covert_to_int(clf):
    if clf==1:
        clf="cancer"
        return clf
    else:
        clf="No Cancer"
        return clf


def diabetes_covert_to_int(clf):
    if clf==1:
        clf="Has Diabetes"
        return clf
    else:
        clf="Has No Diabetes"
        return clf