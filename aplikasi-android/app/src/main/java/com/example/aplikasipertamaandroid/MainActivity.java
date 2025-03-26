package com.example.aplikasipertamaandroid;

import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.graphics.Insets;
import androidx.core.view.ViewCompat;
import androidx.core.view.WindowInsetsCompat;

public class MainActivity extends AppCompatActivity {

  private EditText editText1, editText2;
  private Spinner spinner;
  private TextView textViewResult;
  private Button buttonCalculate;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    setContentView(R.layout.activity_main);

    // Inisialisasi komponen
    editText1 = findViewById(R.id.editText1);
    editText2 = findViewById(R.id.editTextNumber2);
    spinner = findViewById(R.id.spinner);
    textViewResult = findViewById(R.id.textView);
    buttonCalculate = findViewById(R.id.button);

    // Set listener untuk window insets
    ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main), (v, insets) -> {
      Insets systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars());
      v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom);
      return insets;
    });

    // Isi Spinner dengan operator matematika
    ArrayAdapter<String> adapter = new ArrayAdapter<>(this, android.R.layout.simple_spinner_item, new String[]{"+", "-", "*", "/"});
    adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
    spinner.setAdapter(adapter);


    // Set aksi tombol
    buttonCalculate.setOnClickListener(v -> calculateResult());
  }

  private void calculateResult() {
    String input1 = editText1.getText().toString();
    String input2 = editText2.getText().toString();

    if (input1.isEmpty() || input2.isEmpty()) {
      Toast.makeText(this, "Masukkan kedua bilangan", Toast.LENGTH_SHORT).show();
      return;
    }

    double num1 = Double.parseDouble(input1);
    double num2 = Double.parseDouble(input2);
    String operator = spinner.getSelectedItem().toString();
    double result = 0;

    switch (operator) {
      case "+":
        result = num1 + num2;
        break;
      case "-":
        result = num1 - num2;
        break;
      case "*":
        result = num1 * num2;
        break;
      case "/":
        if (num2 != 0) {
          result = num1 / num2;
        } else {
          Toast.makeText(this, "Tidak dapat membagi dengan nol", Toast.LENGTH_SHORT).show();
          return;
        }
        break;
    }

    textViewResult.setText(String.valueOf(result));
  }
}
