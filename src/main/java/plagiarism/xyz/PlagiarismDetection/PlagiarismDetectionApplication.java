package plagiarism.xyz.PlagiarismDetection;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class PlagiarismDetectionApplication {
	public static void main(String[] args) {
		// int[][] a = new int[3][2];
		// int[][] b = new int[2][3];
		// {{0},
		//  {0},
		//  {0}};

		// {
		//   {0, 0, 0}
		// };

		// int[][] p = {
		// 	{1, 2, 3},
		// 	{2, 4, 6},
		// 	{3, 6, 9}
		// };

		// for (int i = 0; i < 3; i++) {
		// 	for (int j = 0; j < 3; j++) {
		// 		for (int k = 0; k < 2; k++) {
		// 			p[i][j] = p[i][j] + a[i][k] * b[k][j];
		// 		}
		// 	}
		// }

		// for (int i = 0; i < 3; i++) {
		// 	for (int j = 0; j < 3; j++) {
		// 		System.out.println("{" + p[i][j]);
		// 	}
		// }

		SpringApplication.run(PlagiarismDetectionApplication.class, args);
	}

}
