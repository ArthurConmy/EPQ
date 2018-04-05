#include <iostream>
#include <cmath>

using namespace std;

typedef long long ll;

bool P(ll F, ll I)
{
	//cout << F << " " << I << endl;

	if (I == pow(2, F - 1)) return 1;

	if (I < pow(2, F - 1)) return P(F-1, I);

	return !P(F, pow(2, F) - I);
}

int main()
{
	/*for (int f = 1; f <= 4; f++)
	{
		for (int c = 1; c < pow(2, f); c++)
		{
			cout << P(f, c);
		}

		cout << endl;
	}*/

	ll f, c;
	cin >> f >> c;

	if (P(f, c)) cout << "D";
	else cout << "U";

	if (P(f, c+1)) cout << "D";
	else cout << "U";

	if (P(f, c+2)) cout << "D";
	else cout << "U";

	cout << endl;

	cin >> f; // to stop insta-close

	return 0;
}