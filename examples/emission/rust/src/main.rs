//! Calling the spaceemit electron-emission API from Rust.
//!
//! ```text
//! cargo run                                        # public instance
//! SPACEEMIT_URL=http://localhost:8741 cargo run    # your own spaceemit
//! ```

use serde::{Deserialize, Serialize};

/// `POST /v1/emission` request. Every numeric field may also be an array (see the API docs);
/// this example uses arrays for `field` and `temperature`.
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct EmissionRequest {
    /// Local field (V/nm).
    field: Vec<f64>,
    /// Radius of curvature (nm); `None` = planar.
    radius: Option<f64>,
    /// Work function (eV).
    work_function: f64,
    /// Temperature (K).
    temperature: Vec<f64>,
}

#[derive(Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
struct EmissionResponse {
    /// A/nm².
    current_density: Vec<Option<f64>>,
    /// W/nm²; negative = the emitter is heated.
    nottingham_heat: Vec<Option<f64>>,
    /// Mean emitted energy relative to E_F (eV).
    mean_energy: Vec<Option<f64>>,
    regime: Vec<Option<String>>,
    errors: Vec<PointError>,
}

#[derive(Deserialize, Debug)]
struct PointError {
    index: usize,
    code: String,
    message: String,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let url = std::env::var("SPACEEMIT_URL").unwrap_or_else(|_| "https://spaceemit-api.sliplane.app".into());

    let request = EmissionRequest {
        field: vec![3.0, 5.0, 8.0],
        radius: Some(50.0),
        work_function: 4.5,
        temperature: vec![300.0, 1000.0, 2000.0],
    };
    let response: EmissionResponse = ureq::post(format!("{url}/v1/emission"))
        .send_json(&request)?
        .body_mut()
        .read_json()?;

    for (i, field) in request.field.iter().enumerate() {
        match (response.current_density[i], response.nottingham_heat[i], response.mean_energy[i]) {
            (Some(j), Some(p), Some(e)) => println!(
                "F = {field} V/nm, T = {} K: J = {j:.3e} A/nm², P_N = {p:.3e} W/nm², <E - E_F> = {e:+.3} eV ({})",
                request.temperature[i],
                response.regime[i].as_deref().unwrap_or("?"),
            ),
            _ => println!("F = {field} V/nm: no result"),
        }
    }
    for e in &response.errors {
        eprintln!("point {} failed: {} ({})", e.index, e.code, e.message);
    }
    Ok(())
}
