package dev.abrown.pilawnmower

import android.Manifest
import android.annotation.SuppressLint
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.util.Log
import android.view.Menu
import android.view.MenuItem
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.google.android.gms.location.FusedLocationProviderClient
import com.google.android.gms.location.LocationServices

import com.google.android.gms.maps.CameraUpdateFactory
import com.google.android.gms.maps.GoogleMap
import com.google.android.gms.maps.OnMapReadyCallback
import com.google.android.gms.maps.SupportMapFragment
import com.google.android.gms.maps.model.LatLng
import com.google.android.gms.maps.model.Polygon
import com.google.android.gms.maps.model.PolygonOptions
import com.google.android.material.snackbar.BaseTransientBottomBar
import com.google.android.material.snackbar.Snackbar
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.async
import kotlinx.coroutines.launch
import java.nio.ByteBuffer
import java.util.concurrent.Future

class MapsActivity : AppCompatActivity(), OnMapReadyCallback {

    companion object {
        private const val FINE_LOCATION_REQUEST_CODE = 0
        private const val BLUETOOTH_REQUEST_CODE = 1
    }

    private lateinit var mMap: GoogleMap
    private lateinit var fusedLocationClient: FusedLocationProviderClient

    private val locationHistory = mutableListOf<Location>()
    private var trackLocation = false
    private val bluetoothService = MowerBluetoothService()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_maps)

        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        val mapFragment = supportFragmentManager
                .findFragmentById(R.id.map) as SupportMapFragment
        mapFragment.getMapAsync(this)

        val button = findViewById<Button>(R.id.button_track_location)
        button.setOnClickListener {
            if (trackLocation) {
                button.text = "Start"
                trackLocation = false
            } else {
                button.text = "Stop"
                locationHistory.clear()
                trackLocation = true
            }
        }

        registerReceiver(bluetoothService, IntentFilter(BluetoothDevice.ACTION_FOUND))
        fusedLocationClient = LocationServices.getFusedLocationProviderClient(this)
    }

    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    override fun onMapReady(googleMap: GoogleMap) {
        mMap = googleMap
        mMap.mapType = GoogleMap.MAP_TYPE_SATELLITE


        getLocationPermission()
    }

    private fun getLocationPermission() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            if (ActivityCompat.shouldShowRequestPermissionRationale(this, Manifest.permission.ACCESS_FINE_LOCATION)) {
                Snackbar.make(findViewById<View>(R.id.map), "You have to enable location...", Snackbar.LENGTH_INDEFINITE)
                        .setAction("OK") {
                            ActivityCompat.requestPermissions(this,
                                    arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), FINE_LOCATION_REQUEST_CODE)
                        }
            } else {
                ActivityCompat.requestPermissions(this,
                        arrayOf(Manifest.permission.ACCESS_FINE_LOCATION), FINE_LOCATION_REQUEST_CODE)
            }
        } else {
            doMapStuff()
        }
    }

    @SuppressLint("MissingPermission")
    private fun doMapStuff() {

        mMap.isMyLocationEnabled = true

        fusedLocationClient.lastLocation.addOnSuccessListener {
            mMap.moveCamera(CameraUpdateFactory
                .newLatLngZoom(LatLng(it.latitude, it.longitude), 25f))
        }

        val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager

        val locationListener = object : LocationListener {

            var polygon: Polygon? = null

            override fun onStatusChanged(provider: String?, status: Int, extras: Bundle?) {
            }

            override fun onProviderEnabled(provider: String?) {
            }

            override fun onProviderDisabled(provider: String?) {
            }

            override fun onLocationChanged(location: Location) {
                if (trackLocation) {
                    locationHistory.add(location)
                    if (polygon != null) {
                        polygon!!.remove()
                    }
                    val polygonOptions = PolygonOptions().fillColor(R.attr.colorAccent).strokeColor(R.attr.colorPrimary)
                    locationHistory.forEach {
                        polygonOptions.add(LatLng(it.latitude, it.longitude))
                    }
                    polygon = mMap.addPolygon(polygonOptions)

                }
            }
        }

        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 0, 0f, locationListener)

    }

    private fun sendLocationData() {

        if (bluetoothService.checkPermission() == false) {
            val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
            startActivityForResult(enableBtIntent, BLUETOOTH_REQUEST_CODE)
        }
        else {

            // Show spinner
            val spinner = findViewById<ProgressBar>(R.id.bluetooth_progress)
            spinner.visibility = View.VISIBLE

            val snackbar = Snackbar.make(spinner, "Transmitting region to LawnBuddy Mower...", Snackbar.LENGTH_INDEFINITE)
            snackbar.show()

            Log.i("MapsAcitivity", locationHistory.toString())

            // Do the work
            GlobalScope.launch {
                try {
                    bluetoothService.connectToMower()

                    // Send number of location points first
                    val size = locationHistory.size.bytes()
                    bluetoothService.sendToMower(size)

                    // Send all the location points
                    for (location in locationHistory) {
                        bluetoothService.sendToMower(location.latitude.bytes())
                        bluetoothService.sendToMower(location.longitude.bytes())
                    }

                    bluetoothService.sendToMower("q".toByteArray())
                    snackbar.dismiss()
                } catch (e: Exception) {
                    snackbar.dismiss()
                    Snackbar.make(spinner, "Error sending region to LawnBuddy. Make sure Bluetooth is on and PiLawnMower is paired.", Snackbar.LENGTH_SHORT).show()
                } finally {
                    // When Done, rid of spinner
                    spinner.visibility = View.INVISIBLE
                }

            }
        }

    }

    fun Int.bytes() =
        ByteBuffer.allocate(kotlin.Int.SIZE_BYTES)
            .putInt(this)
            .array()

    fun Double.bytes() =
        ByteBuffer.allocate(java.lang.Long.BYTES)
            .putLong(java.lang.Double.doubleToLongBits(this))
            .array()


    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        when (requestCode) {
            FINE_LOCATION_REQUEST_CODE -> {
                if ((grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED)) {
                    doMapStuff()
                }
                return
            }
            BLUETOOTH_REQUEST_CODE -> {
                if ((grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED)) {
                    sendLocationData()
                }
                return
            }
            else -> {

            }
        }
    }

    override fun onCreateOptionsMenu(menu: Menu?): Boolean {
        menuInflater.inflate(R.menu.menu, menu)

        return true
    }

    override fun onOptionsItemSelected(item: MenuItem) = when (item.itemId) {
        R.id.action_export -> {
            sendLocationData()
            true
        }

        else -> {
            // If we got here, the user's action was not recognized.
            // Invoke the superclass to handle it.
            super.onOptionsItemSelected(item)
        }
    }

}
