for item in my_list:
    if item.flavor == 'banana':
        break
    else:
        raise ValueError('No banana flavor found!')
