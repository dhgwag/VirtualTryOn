# VirtualTryOn

## User Manual
### Test

*Test에는 conda 환경설정이 필요하지 않습니다.*  
*test.py option에서 각 python 경로 설정 필요*


> ##### Step1
> *input image에서 배경을 삭제하는 단계*
> > Dataset :   
> > copy images into **datasets/org_img** folder
>    
> > run :   
> > ```
> > python test.py --step step1
> > ```
>  
> > result :   
> > **output/background_step1** 에 생성
   
> ##### Step2
> *model의 위치를 중간으로 옮기고, openpose data를 생성하는 단계*   
> *현재 서버 세팅이 되지 않아, 로컬 코드 상태이고 서버에서는 동작 안함*
> > Dataset :   
> > copy step1 output images into **input_path** folder
>    
> > run :   
> > ```
> > python test.py --step step2 [현재 동작 안함]
> > ```
> > or   
> > ```
> > python openpose/test.py
> > ```
>  
> > result :   
> > **output_img** 에 중점 이동 후 size 조정한 이미지 생성   
> > **output_pose** 에 openpose 이미지 생성   
> > **output_posejson** 에 openpose json data 생성
>  
> > reference :   
> > <https://github.com/CMU-Perceptual-Computing-Lab/openpose>

> ##### Step3
> *model segment generation*
> > Dataset :   
> > step2 **output_img** output을 **datasets/image** folder로 copy
> > **datasets/labels**와 **datasets/edges** 에 **512x512.png** 필요   
> > **datasets/val.txt** 에 generation할 image 와 label 경로 입력 (label은 고정값을 넣어주면 됨)
> > **datasets/val_id.txt** 에 input edge 경로 입력 (고정값을 넣어주면 됨, 다만 image 개수와 일치 필요)
> > **datasets/palette_ref.png** 필요 (palette 참고용)
>    
> > run :   
> > ```
> > python test.py --step step3
> > ```
>  
> > result :   
> > **output/cihp_parsing** 에 결과 이미지 생성   
>  
> > reference :   
> > <https://github.com/Engineering-Course/CIHP_PGN>

> ##### Step4
> *cloth synthesis[VITON-HD]*
> > Dataset :   
> > step2 **output_pose** output을 **datasets/openpose-img** folder로 copy   
> > step2 **output_posejson** output을 **datasets/openpose-json** folder로 copy   
> > **datasets/cloth** folder에 합성할 cloth image copy   
> > **datasets/cloth-mask** folder에 합성할 cloth-mask image copy   
> > **datasets/test_pairs.txt** 에 합성할 model과 cloth의 pair를 작성  
>    
> > run :   
> > ```
> > python test.py --step step4
> > ```
>  
> > result :   
> > **output/viton-hd** 에 결과 이미지 생성   

> ##### Step5
> *background synthesis*
> > Dataset :   
> > **datasets/bg_images** folder에 합성할 background image와 model position info txt copy   
> > **datasets/backgrounds.txt** 에 합성할 background과 position txt file path 작성  
>    
> > run :   
> > ```
> > python test.py --step step5
> > ```
>  
> > result :   
> > **output/final** 에 결과 이미지 생성   

### Train
*기본 경로 : VITON-HD*  
Conda Env Activation :
```
conda activate VITON_HD
```
   
*Preprocessing*
1. cloth와 cloth-mask 이미지 size 조정 (512x512)   
2. model image를 중점으로 이동시키고 size 조정 (512x512)   
3. 2에서 만든 image로 parse map과(segment) openpose 데이터 추출   
4. 학습할 model과 cloth pair를 **datasets/train_pairs.txt**에 작성   
   
   
> ##### Seg Generation
> > Dataset :   
> > **datasets/train/cloth** folder에 학습할 cloth copy   
> > **datasets/train/cloth-mask** folder에 학습할 cloth mask copy   
> > **datasets/train/image-parse** folder에 에 parse map(segment) copy   
> > **datasets/train/openpose-img** folder에 에 openpose image copy   
> > **datasets/train/openpose-json** folder에 에 openpose json copy   
>    
> > run :   
> > ```
> > python train.py --train_model seg --name [테스트 이름]
> > ```
>  
> > result :   
> > **checkpoints/[테스트 이름]** 에 생성
   
> ##### Gmm Generation
> > Dataset :   
> > **datasets/train/image** folder에 학습할 model image copy
>    
> > run :   
> > ```
> > python train.py --train_model gmm --name [테스트 이름]
> > ```
>  
> > result :   
> > **checkpoints/[테스트 이름]** 에 생성

   
> ##### Alias Generation
> > Dataset :   
> > GMM 학습 결과로 만들어낸 warped cloth를 **datasets/train/warped_cloth** folder에 copy   
> > GMM 학습 결과로 만들어낸 warped cloth-mask를 **datasets/train/warped_cloth-mask** folder에 copy   
>    
> > run :   
> > ```
> > python train.py --train_model alias --name [테스트 이름]
> > ```
>  
> > result :   
> > **checkpoints/[테스트 이름]** 에 생성
   
***
## Q&A
- input image의 background를 재사용하려면?   
  - Step1에서 배경제거를 할 때 model의 position 정보를 읽은 후, 해당 정보를 Step5에 사용되는 model position txt파일로 저장   
  - Step5에서 input background에 원본 이미지를 사용   
  - 혹은 background/demo.py 내에서 좌표값 넣는 부분을 직접 수정해도 가능
- 하의를 학습하려면 뭘 바꿔야 하는지?   
  - train_dataset.py & test_datset.py
     - get_parse_agnostic() 에서 masking하는 부분을 상의에서 하의로 수정
     - get_img_agnostic() 에서 masking하는 부분을 상의에서 하의로 수정
  - VitonHDModel.py
     - GmmModel() class의 forward()에서 parse_map[] 곱셈 연산하는 부분 상의에서 하의로 parameter 변경
     - AliasModel() class의 forward()에서 alias_parse[] 곱셈 연산하는 부분 상의에서 하의로 parameter 변경
- 3차, 4차, 5차 학습의 차이점
   - 파라미터 외에는 큰 차이 없음
   - 4차는 GAN Loss 연산에서 target_is_real param에 False를 넣었는데, 결과적으로 True를 넣은 3차 및 5차 결과가 훨씬 좋았음
   - 3차와 5차의 차이는 GAN feature matching loss의 lambda 값임 (3차는 5, 5차는 10)
- 개발 과정에서의 문제점과 한계
  - Dataset issue
     - 고해상도의 이미지를 구하기가 어려워 학습결과도 해상도가 좋지 않음. 이미지는 512x512지만, 옷이 차지하는 영역이 작아서 사실상 저해상도
     - 다양하지 않은 옷. 피부가 많이 노출되는 반팔셔츠, 나시 등의 데이터셋이 많지 않아 피부를 생성해내는 능력이 많이 떨어짐
     - 데이터셋의 개수가 15000장 정도로 충분히 많지 않음
     - 팔을 들고 있는 자세, 팔이 꼬인 자세 등 복잡한 자세를 가진 이미지로 인해 학습 정확도가 떨어짐
- 개선 가능한 사항
   - Gmm 개선
     - second-order difference constraint로 인해 옷의 뒤틀림 현상을 개선했지만, 그와 동시에 원하는 자세로 온전히 warping시키지 못한다는 문제가 있었음
     - 기존 gmm과 달리, model의 자세에 더 맞게끔 warping시킬 수 있다면 훨씬 좋은 성능이 나올것으로 기대함
   
***
   
## Contact
곽동훈   
Tel : 010-7449-0360   
e-mail : Donghoon.Gwag@gmail.com
