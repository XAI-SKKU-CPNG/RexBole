import React from 'react'
import ProductCard from './ProductCard'
import { RecommendationsOut } from '../../client'

// interface Product {
//   id: number
//   title: string
//   price: string
//   rating: number
//   reviews: number
//   isRocket: boolean
// }

// const products: Product[] = [
//   {
//     id: 1,
//     title: '코디코치 깔끔 팬츠 면 통 일자 남자 와이드 롱 베이직 통넓은 바지',
//     price: '29,900원',
//     rating: 5,
//     reviews: 255,
//     isRocket: true,
//   },
//   {
//     id: 2,
//     title: '로니제이 남녀공용 와이드핏 조거 Y2K 카고 팬츠',
//     price: '24,900원',
//     rating: 5,
//     reviews: 492,
//     isRocket: true,
//   },
//   {
//     id: 3,
//     title:
//       '에스티오 2in1투웨이 M~2XL 밑단 조임 사이드핀턱 벌룬트레이닝 팬츠 밑단스트링',
//     price: '34,900원',
//     rating: 5,
//     reviews: 88,
//     isRocket: true,
//   },
//   {
//     id: 4,
//     title:
//       '남여공용 빅사이즈 더블턱 와이드 슬랙스 링클프리 남자 팬츠 바지 (4color)',
//     price: '29,900원',
//     rating: 5,
//     reviews: 102,
//     isRocket: true,
//   },
//   {
//     id: 5,
//     title:
//       '굿럭샵 와이드 츄리닝 -130kg 까지 남자 여자 빅사이즈 트레이닝 운동복 바지 L-XXXXXL 2345XL',
//     price: '23,900원',
//     rating: 5,
//     reviews: 1249,
//     isRocket: false,
//   },
// ]

const ProductList: React.FC<RecommendationsOut> = ({
  data: recommendationsData,
  // count: recommendationsCount,
}) => {
  return (
    <div className="grid grid-cols-3 gap-4">
      {recommendationsData.map((recommendation) => (
        <ProductCard
          key={recommendation.rec_item_id}
          recommendation={recommendation}
        />
      ))}
    </div>
  )
}

export default ProductList
