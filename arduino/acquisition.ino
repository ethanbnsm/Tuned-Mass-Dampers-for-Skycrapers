// acquisition.ino
// Lecture de l'axe X de l'accéléromètre et conversion en g

const int xpin = A0;    // entrée analogique
int xvalue;

void setup() {
  Serial.begin(9600);
}

void loop() {
  // lire la valeur brute
  xvalue = analogRead(xpin);

  // ramener la valeur brute calibrée (267–347) en [-300 ; +300]
  int x = map(xvalue, 267, 347, -300, 300);

  // convertir en g et recentrer verticalement
  float xg = ((float)x / (-300.00)) - 2.22;

  // envoyer en série
  Serial.println(xg);

  // pause 10 ms entre deux mesures
  delay(10);
}
