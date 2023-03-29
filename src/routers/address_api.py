import logging
import geopy.distance
from datetime import datetime
from fastapi import APIRouter
from fastapi import status, HTTPException, Response, Depends
from sqlalchemy.orm import Session

from src.db.models.address import Address
from src.db.session import get_db
import traceback

from . import schemas

router = APIRouter(
    prefix='/v1.0/address',
        tags=['Address Management']
    )


@router.get('/get_address/{user_id}', status_code=status.HTTP_200_OK)
def get_address_details(user_id, db: Session=Depends(get_db)):
    try:
        user_address_details = db.query(Address).filter(Address.user_id == user_id).first()
        if not user_address_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "user not found")
        output_json = {
            "Address": user_address_details.address_body,
            "Co-ordinates": user_address_details.coordinates
        }
        return output_json
    except Exception as exception:
        logging.error(exception)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in getting address Details. ")
    

@router.get('/distance_based_addresses/{user_id}', status_code=status.HTTP_200_OK)
def get_address_details(user_id, distance_in_kms:int, db: Session=Depends(get_db)):
    try:
        final_list = []
        user_address_details = db.query(Address).filter(Address.user_id == user_id).first()
        all_user_address = db.query(Address).all()
        if not user_address_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "user not found")
        user_coordinate = user_address_details.coordinates.replace('(','').replace(')','')
        user_coordinate = user_coordinate.split(',')
        user_coordinate_tup = (float(user_coordinate[0]),float(user_coordinate[1]))
        for data in all_user_address:
            db_coordinates = data.coordinates
            coordinates = data.coordinates.replace('(','').replace(')','')
            coordinates = coordinates.split(',')
            coordinate_tup = (float(coordinates[0]),float(coordinates[1]))
            if geopy.distance.geodesic(user_coordinate_tup, coordinate_tup) <= distance_in_kms:
                final_list.append({
                    "Address": db.query(Address).filter(Address.coordinates == db_coordinates).first().address_body,
                    "Co-ordinates": db_coordinates
                    }
                )

        output_json = {
            "required_addresses": final_list
        }
        return output_json
    except Exception as exception:
        logging.error(exception)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in getting address Details. ")


@router.post('/save_address', status_code=status.HTTP_200_OK)
def save_address_details(request:schemas.PostAddress, coordinates: str='', db: Session=Depends(get_db)):
    try:

        latlng = [eval(i) for i in coordinates.replace(" ","").split()]
        loc_lon = latlng[0][1]
        loc_lat = latlng[0][0]

        if (loc_lat > 90.0) or (loc_lat < -90.0):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="latitude should be between 90 and -90.")
        
        if (loc_lon > 180.0) or (loc_lat < -180.0):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="longitude should be between 180 and -180.")
        
        new_address = Address(address_body=request.full_address, coordinates=coordinates,user_id=request.user_id)
        db.add(new_address)
        db.commit()
        db.refresh(new_address)
        db.close()
        return "User address added successfully"
    except Exception as exception:
        logging.error(exception)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in saving user address details")
    

@router.put('/update_address/{user_id}', status_code=status.HTTP_200_OK)
def update_address_details(user_id, request:schemas.UpdateAddress, coordinates: str='', db: Session=Depends(get_db)):
    try:
        if coordinates != '':
            latlng = [eval(i) for i in coordinates.replace(" ","").split()]
            loc_lon = latlng[0][1]
            loc_lat = latlng[0][0]

            if (loc_lat > 90.0) or (loc_lat < -90.0):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="latitude should be between 90 and -90.")
            
            if (loc_lon > 180.0) or (loc_lat < -180.0):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="longitude should be between 180 and -180.")
        
            address_id = db.query(Address).filter(Address.user_id == user_id).first().id
            db_address = db.get(Address, address_id)
            db_address.coordinates = coordinates
            db_address.address_body = request.full_address
            db_address.updated_on = datetime.utcnow
            db.add(db_address)
            db.commit()
            db.refresh(db_address)
            db.close()
        else:
            address_id = db.query(Address).filter(Address.user_id == user_id).first().id
            db_address = db.get(Address, address_id)
            db_address.address_body = request.full_address
            db_address.updated_on = datetime.utcnow
            db.add(db_address)
            db.commit()
            db.refresh(db_address)
            db.close()
        return "User address updated successfully"
    except Exception as exception:
        logging.error(exception)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in updating user address details")


@router.delete('/delete_address/{user_id}', status_code=status.HTTP_200_OK)
def removeVaultDetails(user_id, db: Session=Depends(get_db)):
    try:
        address_id = db.query(Address).filter(Address.user_id == user_id).first().id
        db_delete_address = db.get(Address, address_id)
        db.delete(db_delete_address)
        db.commit()
        db.close()
        return "Address for the user is deleted successfully."
    except Exception as exception:
        logging.error(exception)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in removing address details.")