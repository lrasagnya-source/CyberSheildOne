# pages/qr_scanner.py

import streamlit as st

from services.qr_service import decode_qr_image

from services.url_service import detect_fake_url


st.title("📱 QR Code Security Scanner")

st.write(
    "Upload a QR code image to extract and analyze its content."
)


uploaded_file = st.file_uploader(
    "Upload a QR Code Image",
    type=["png", "jpg", "jpeg"]
)


if uploaded_file is not None:

    st.image(
        uploaded_file,
        caption="Uploaded QR Code",
        width=300
    )


if st.button("🔍 Scan QR Code"):

    if uploaded_file is None:

        st.warning(
            "Please upload a QR code image first."
        )

    else:

        # Step 1: Decode QR code
        qr_result = decode_qr_image(
            uploaded_file
        )

        if not qr_result["success"]:

            st.error(
                qr_result["message"]
            )

        else:

            extracted_data = qr_result["data"]

            st.success(
                "✅ QR Code Successfully Scanned"
            )

            st.subheader(
                "📄 QR Code Content"
            )

            st.code(
                extracted_data
            )

            # Check if QR content is a URL
            if extracted_data.startswith(
                ("http://", "https://", "www.")
            ):

                st.subheader(
                    "🌐 URL Security Analysis"
                )

                # Analyze URL using existing URL service
                result = analyze_url(
                    extracted_data
                )

                risk_score = result["risk_score"]

                security_score = 100 - risk_score

                # Save QR security score for dashboard
                st.session_state[
                    "qr_score"
                ] = security_score

                # Display result
                if risk_score >= 60:

                    st.error(
                        "🚨 DANGEROUS QR CODE"
                    )

                elif risk_score >= 30:

                    st.warning(
                        "⚠️ SUSPICIOUS QR CODE"
                    )

                else:

                    st.success(
                        "✅ QR CODE APPEARS SAFE"
                    )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Risk Score",
                        f"{risk_score}/100"
                    )

                with col2:

                    st.metric(
                        "Security Score",
                        f"{security_score}/100"
                    )

                if result.get(
                    "reasons"
                ):

                    st.subheader(
                        "🔎 Detected Indicators"
                    )

                    for reason in result[
                        "reasons"
                    ]:

                        st.write(
                            f"• {reason}"
                        )

            else:

                st.info(
                    "This QR code does not contain a website URL."
                )