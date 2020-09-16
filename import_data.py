import pandas as pd

def import_main_dataset():
    df=pd.read_csv(
        'spanish_houses.csv',
        dtype={
            'subtitle':str,
            'sq_mt_built':float,
            'n_rooms':int,
            'n_bathrooms':float,
            'buy_price':int,
            'buy_price_by_area':int,
            'house_type_id':str,
            'is_renewal_needed':bool,
            'is_new_development':bool,
            'has_lift':bool,
            'is_exterior':bool,
            'has_parking':bool
        }
    )
    df.columns=['Neighborhood','Total area (m2)','Number of rooms','Number of bathrooms',
                'Price (euro)','Price for m2 (euro)','House type','Is renewal needed',
                'Is new development','Has lift','Is exterior','Has parking']
    return df
