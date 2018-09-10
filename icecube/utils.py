def get_cuts_tag(tod_data):
    """A utility function that gets the cuts tag for the TOD"""
    tod_info = tod_data.info
    
    # Get array name
    array_name = tod_info.array
    
    if array_name == 'ar4':
        tag = "pa4_f150_s17_c10_v4"
    elif array_name == 'ar5':
        tag = "pa5_f150_s17_c10_v6"
    elif array_name == 'ar6':
        tag = "pa6_f150_s17_c10_v6"
    else:
        raise "Wrong array!"
    return tag

def get_pointing_par(tod_data):
    """A utility function that gets the pointing par for the TOD"""
    tod_info = tod_data.info

    # Get array name
    array_name = tod_info.array
    if array_name == 'ar4':
        filename = "/mnt/act3/users/mhasse/depots/shared/RelativeOffsets/template_ar4_180303.txt"
    elif array_name == 'ar5':
        filename = "/mnt/act3/users/mhasse/depots/shared/RelativeOffsets/template_ar5_180303.txt"
    elif array_name == 'ar6':
        filename = "/mnt/act3/users/mhasse/depots/shared/RelativeOffsets/template_ar6_180303.txt"
    else:
        raise "Wrong array!"

    pointpar = {'source': 'fp_file',\
                'filename': filename}

    return pointpar
