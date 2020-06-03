package dev.abrown.pilawnmower

import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.async
import java.io.IOException
import java.util.*
import java.util.concurrent.Future

class MowerBluetoothService :BroadcastReceiver() {

    val bluetoothAdapter = BluetoothAdapter.getDefaultAdapter()

    private var connectedDevice: BluetoothDevice? = null
    private var socket: BluetoothSocket? = null

    fun checkPermission() = bluetoothAdapter?.isEnabled

    fun connectToMower() {
        bluetoothAdapter?.bondedDevices?.forEach { device ->
            Log.d("BluetoothService", "BondedDevice: ${device.name}")
            if (device.name == "PiLawnMower") {
                bluetoothAdapter.cancelDiscovery()
                connectedDevice = device
                socket = device.createRfcommSocketToServiceRecord(UUID.fromString("94f39d29-7d6d-437d-973b-fba39e49d4ee"))
                socket!!.connect()
            }
        }
    }

    fun sendToMower(bytes: ByteArray) {
        try {
            socket!!.outputStream.write(bytes)
        } catch (e: IOException) {
            Log.e("BluetoothService", "Error occurred when sending data", e)
        }
    }

    fun disconnectFromMower() {
        try {
            socket?.close()
        } catch (e: IOException) {
            Log.e("BluetoothService", "Could not close the client socket", e)
        }
    }

    override fun onReceive(p0: Context?, p1: Intent?) {

    }



}