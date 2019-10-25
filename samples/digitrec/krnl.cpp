#include <string.h>
#include <math.h>
#include <assert.h>
#pragma ACCEL kernel
void default_function(unsigned long test_image, unsigned long train_images[10][1800], unsigned char knn_mat[10][3]) {
  unsigned char knn_mat_buf[10][4];
#pragma ACCEL parallel
  for (int x = 0; x < 10; ++x) {
    for (int y = 0; y < 4; ++y) {
      knn_mat_buf[x][y] = (unsigned char)50;
    }
  }
  unsigned long knn_update;
#pragma ACCEL pipeline
  for (int y1 = 0; y1 < 1800; ++y1) {
#pragma ACCEL parallel
    for (int x1 = 0; x1 < 10; ++x1) {
      unsigned char dist;
      unsigned long diff;
      diff = (train_images[x1][y1] ^ test_image);
      unsigned char out;
      out = (unsigned char)0;
#pragma ACCEL parallel
      for (int i = 0; i < 49; ++i) {
        out = ((unsigned char)(((unsigned long)out) + ((unsigned long)((diff & (1L << i)) >> i))));
      }
      dist = out;
      unsigned long max_id;
      max_id = (unsigned long)0;
      for (int i1 = 0; i1 < 3; ++i1) {
        if (knn_mat_buf[((((long)max_id) + ((long)(x1 * 4))) / (long)4)][((((long)max_id) + ((long)(x1 * 4))) % (long)4)] < knn_mat_buf[x1][i1]) {
          max_id = ((unsigned long)i1);
        }
      }
      if (dist < knn_mat_buf[((((long)max_id) + ((long)(x1 * 4))) / (long)4)][((((long)max_id) + ((long)(x1 * 4))) % (long)4)]) {
        knn_mat_buf[((((long)max_id) + ((long)(x1 * 4))) / (long)4)][((((long)max_id) + ((long)(x1 * 4))) % (long)4)] = dist;
      }
    }
  }
  for (int x2 = 0; x2 < 10; ++x2) {
    for (int y2 = 0; y2 < 3; ++y2) {
      knn_mat[x2][y2] = knn_mat_buf[x2][y2];
    }
  }
}

