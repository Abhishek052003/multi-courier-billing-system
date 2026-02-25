from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import io
from services.franch_service import calculate_franch_rate, load_all_rates
from services.professional_service import calculate_professional_rate, load_all_professional_rates
from services.professional_kolkata_service import (
    calculate_professional_kolkata_rate,
    load_all_professional_kolkata_rates
)
from services.trackon_east_service import (
    calculate_trackon_east_rate,
    load_all_trackon_east_rates
)


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.post("/upload/franch")
async def upload_franch_file(file: UploadFile = File(...)):

    try:
        # Read uploaded file
        contents = await file.read()

        # Load into pandas
        df = pd.read_excel(io.BytesIO(contents))

        # Validate required columns
        required_columns = ["City", "Weight"]
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(status_code=400, detail=f"Missing column: {col}")

        rate_dict = load_all_rates()
        rounded_weights = []
        final_rates = []

        

        # Process each row
        for index, row in df.iterrows():

            # Validate City
            if pd.isna(row["City"]):
                raise HTTPException(
                    status_code=400,
                    detail=f"City is missing at row {index + 2}"
                )

            # Validate Weight
            if pd.isna(row["Weight"]):
                raise HTTPException(
                    status_code=400,
                    detail=f"Weight is missing at row {index + 2}"
                )

            zone = str(row["City"])
            
            try:
                weight = float(row["Weight"])
            except:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid weight value at row {index + 2}"
                )

            rounded, rate = calculate_franch_rate(zone, weight, rate_dict)

            rounded_weights.append(rounded)
            final_rates.append(rate)

        df["Rounded_Weight"] = rounded_weights
        df["Calculated_Rate"] = final_rates

        # Save to Excel in memory
        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=franch_billing_output.xlsx"
            }
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/upload/professional")
async def upload_professional_file(file: UploadFile = File(...)):

    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        required_columns = ["City", "Weight"]
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(status_code=400, detail=f"Missing column: {col}")

        # 🔥 Load rates once
        rate_dict = load_all_professional_rates()

        rounded_weights = []
        final_rates = []

        for index, row in df.iterrows():

            if pd.isna(row["City"]):
                raise HTTPException(
                    status_code=400,
                    detail=f"City missing at row {index + 2}"
                )

            if pd.isna(row["Weight"]):
                raise HTTPException(
                    status_code=400,
                    detail=f"Weight missing at row {index + 2}"
                )

            city = str(row["City"])

            try:
                weight = float(row["Weight"])
            except:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid weight at row {index + 2}"
                )

            rounded, rate = calculate_professional_rate(city, weight, rate_dict)

            rounded_weights.append(rounded)
            final_rates.append(rate)

        df["Rounded_Weight"] = rounded_weights
        df["Calculated_Rate"] = final_rates

        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=professional_billing_output.xlsx"
            }
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload/professional_kolkata")
async def upload_professional_kolkata_file(file: UploadFile = File(...)):

    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        required_columns = ["City", "State", "Weight"]
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing column: {col}"
                )

        # 🔥 Load rates once
        rate_dict = load_all_professional_kolkata_rates()

        rounded_weights = []
        final_rates = []

        for index, row in df.iterrows():

            if pd.isna(row["City"]):
                raise HTTPException(
                    status_code=400,
                    detail=f"City missing at row {index + 2}"
                )

            if pd.isna(row["State"]):
                raise HTTPException(
                    status_code=400,
                    detail=f"State missing at row {index + 2}"
                )

            if pd.isna(row["Weight"]):
                raise HTTPException(
                    status_code=400,
                    detail=f"Weight missing at row {index + 2}"
                )

            city = str(row["City"])
            state = str(row["State"])

            try:
                weight = float(row["Weight"])
            except:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid weight at row {index + 2}"
                )

            rounded, rate = calculate_professional_kolkata_rate(
                city, state, weight, rate_dict
            )

            rounded_weights.append(rounded)
            final_rates.append(rate)

        df["Rounded_Weight"] = rounded_weights
        df["Calculated_Rate"] = final_rates

        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=professional_kolkata_billing_output.xlsx"
            }
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/upload/trackon_east")
async def upload_trackon_east_file(file: UploadFile = File(...)):

    try:
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))

        required_columns = ["State", "Weight"]
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(
                    status_code=400,
                    detail=f"Missing column: {col}"
                )

        # 🔥 Load rates once
        rate_dict = load_all_trackon_east_rates()

        rounded_weights = []
        final_rates = []

        for index, row in df.iterrows():

            if pd.isna(row["State"]):
                raise HTTPException(
                    status_code=400,
                    detail=f"State missing at row {index + 2}"
                )

            if pd.isna(row["Weight"]):
                raise HTTPException(
                    status_code=400,
                    detail=f"Weight missing at row {index + 2}"
                )

            state = str(row["State"])

            try:
                weight = float(row["Weight"])
            except:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid weight at row {index + 2}"
                )

            rounded, rate = calculate_trackon_east_rate(
                state, weight, rate_dict
            )

            rounded_weights.append(rounded)
            final_rates.append(rate)

        df["Rounded_Weight"] = rounded_weights
        df["Calculated_Rate"] = final_rates

        output = io.BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=trackon_east_billing_output.xlsx"
            }
        )

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))