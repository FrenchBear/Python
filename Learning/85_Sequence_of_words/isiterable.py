# isiterable.py
# Good method to check if object s is iterable: iter(s) should not return an error.
# iter() works if s has only __getitem__, while for abc.Iterable it needs __iter__.
# 2021-05-18    PV

def is_iterable(s) -> bool:
    try:
        _ = iter(s)
    except TypeError:
        return False
    except Exception as ex:
        raise ex
    return True

if __name__ == '__main__':
    print(f'[1,2]:', is_iterable([1, 2]))
    print(f'123:', is_iterable(123))
