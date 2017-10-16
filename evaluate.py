import cv2
import numpy as np
import os

max_label = 1


def fast_hist(a, b, n):
    k = (a >= 0) & (a < n)
    return np.bincount(n * a[k].astype(int) + b[k], minlength=n ** 2).reshape(n, n)


def get_iou(pred, gt):
    if pred.shape != gt.shape:
        print('pred shape', pred.shape, 'gt shape', gt.shape)
    assert (pred.shape == gt.shape)
    gt = gt.astype(np.float32)
    pred = pred.astype(np.float32)

    count = np.zeros((max_label + 1,))
    for j in range(max_label + 1):
        x = np.where(pred == j)
        p_idx_j = set(zip(x[0].tolist(), x[1].tolist()))
        x = np.where(gt == j)
        GT_idx_j = set(zip(x[0].tolist(), x[1].tolist()))
        # pdb.set_trace()
        n_jj = set.intersection(p_idx_j, GT_idx_j)
        u_jj = set.union(p_idx_j, GT_idx_j)

        if len(GT_idx_j) != 0:
            count[j] = float(len(n_jj)) / float(len(u_jj))

    result_class = count
    Aiou = np.sum(result_class[:]) / float(len(np.unique(gt)))

    return Aiou


result_paths = list(map(lambda x: os.path.join('result', x), os.listdir('result')))

gt_paths = list(map(lambda x: os.path.join('gt', x), os.listdir('gt')))

hist = np.zeros((max_label + 1, max_label + 1))
pytorch_list = []
for i in range(len(gt_paths)):
    gt = cv2.imread(gt_paths[i], 0)
    output = cv2.imread(result_paths[i], 0)

    gt = np.where(gt > 100, 1, 0)
    output = np.where(output > 100, 1, 0)

    iou_pytorch = get_iou(output, gt)
    hist += fast_hist(gt.flatten(), output.flatten(), max_label + 1)

    pytorch_list.append(iou_pytorch)

miou = np.diag(hist) / (hist.sum(1) + hist.sum(0) - np.diag(hist))
print("Mean iou = ", np.sum(miou) / len(miou))
