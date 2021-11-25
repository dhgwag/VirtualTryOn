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
> ##### Seg Generation
> > Dataset :   
> > **datasets/org_img** folder
>    
> > run :   
> > ```
> > python test.py --step step1
> > ```
>  
> > result :   
> > **output/background_step1** 에 생성
   
   
   
***
## Q&A
- input image의 background를 재사용하려면?
  - Step1에서 배경제거를 할 때 model의 position 정보를 읽은 후, 해당 정보를 Step5에 사용되는 model position txt파일로 저장
  - Step5에서 input background에 원본 이미지를 사용
  - 혹은 background/demo.py 내에서 좌표값 넣는 부분을 직접 수정해도 가능
- 하의를 학습하려면 뭘 바꿔야 하는지?
  -fdsf 
- 3차, 4차, 5차 학습의 차이점
- 개발 과정에서의 문제점과 한계
  - Dataset의 문제
  - 
