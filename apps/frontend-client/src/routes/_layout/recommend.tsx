import {
  Box,
  Container,
  Flex,
  Spinner,
  Text,
  Spacer,
  IconButton,
  Image,
  Badge,
  Icon,
  Input,
} from '@chakra-ui/react'
import { SearchIcon, BellIcon } from '@chakra-ui/icons'
import { FaShoppingCart } from 'react-icons/fa'

import { createFileRoute } from '@tanstack/react-router'
import AdBanner from '../../components/Common/AdBanner.tsx'
import ProductList from '../../components/Common/ProductList.tsx'

import useCustomToast from '../../hooks/useCustomToast.ts'
import { useQuery } from 'react-query'
import { ApiError, RecommendationsService } from '../../client/index.ts'
export const Route = createFileRoute('/_layout/recommend')({
  component: Dashboard,
})

function Dashboard() {
  const showToast = useCustomToast()
  const {
    data: recommendations,
    isLoading,
    isError,
    error,
  } = useQuery('recommendations', () =>
    RecommendationsService.readRecommendations(),
  )

  if (isError) {
    const errDetail = (error as unknown as ApiError).body?.detail
    showToast('Something went wrong.', `${errDetail}`, 'error')
  }

  return (
    <>
      {isLoading ? (
        // TODO: Add skeleton
        <Flex justify="center" align="center" height="100vh" width="full">
          <Spinner size="xl" color="ui.main" />
        </Flex>
      ) : (
        recommendations && (
          <Container maxW="full" justifyItems="center">
            <Box pt={12} m={4} width={414} height={896}>
              <Box bg="gray.100">
                {/* 상단바 */}
                <Box bg="black" color="white" p={2} textAlign="center">
                  클릭하는 순간,{' '}
                  <Text as="span" color="yellow.300">
                    무료 혜택!
                  </Text>
                </Box>

                {/* 검색 바 */}
                <Flex bg="white" align="center" p={2}>
                  <Text
                    fontSize="2xl"
                    fontWeight="bold"
                    color="orange.400"
                    ml={2}
                    as="div"
                    margin="auto"
                  >
                    RexBole
                  </Text>
                </Flex>

                <Box p={4} bg="white">
                  <Input
                    placeholder="쿠팡에서 검색하세요!"
                    size="lg"
                    borderRadius="md"
                    bg="gray.100"
                  />
                </Box>

                {/* 광고 배너 */}
                <Box p={4} bg="blue.50" textAlign="center">
                  <Image
                    src="banner-image-url"
                    alt="가을 보습 대전"
                    borderRadius="md"
                    mb={2}
                  />
                  <Text fontSize="lg" fontWeight="bold">
                    가을 보습대전
                  </Text>
                  <Text>아모레퍼시픽</Text>
                </Box>

                {/* 아이콘 메뉴 */}
                <Flex justify="space-around" p={4} bg="white">
                  <Box textAlign="center">
                    <Icon boxSize={6} as={FaShoppingCart} />
                    <Text fontSize="xs">자주산상품</Text>
                  </Box>
                  <Box textAlign="center">
                    <Icon boxSize={6} as={FaShoppingCart} />
                    <Text fontSize="xs">쿠팡플레이</Text>
                  </Box>
                  <Box textAlign="center">
                    <Icon boxSize={6} as={FaShoppingCart} />
                    <Text fontSize="xs">로켓프레시</Text>
                  </Box>
                  <Box textAlign="center">
                    <Icon boxSize={6} as={FaShoppingCart} />
                    <Text fontSize="xs">쿠팡이츠</Text>
                  </Box>
                  {/* 추가 메뉴 아이콘 */}
                </Flex>

                {/* 쿠폰 배너 */}
                <Box p={4} bg="yellow.100" textAlign="center">
                  <Text fontSize="lg" fontWeight="bold">
                    지금 와우 가입하면 바로 사용{' '}
                    <Badge colorScheme="red">1만 5천원 쿠폰</Badge> 지급!
                  </Text>
                </Box>

                {/* 상품 추천 섹션 */}
                <Box p={4}>
                  <Flex align="center">
                    <Text fontSize="lg" fontWeight="bold">
                      이 상품 놓치지 마세요!
                    </Text>
                    <Spacer />
                    <Text color="blue.500">더보기 &gt;</Text>
                  </Flex>
                  <Flex mt={4} overflowX="scroll">
                    {/* 상품 이미지 카드들 */}
                    <Box w="150px" mr={4}>
                      <Image src="product1-url" borderRadius="md" />
                    </Box>
                    <Box w="150px" mr={4}>
                      <Image src="product2-url" borderRadius="md" />
                    </Box>
                    <Box w="150px" mr={4}>
                      <Image src="product3-url" borderRadius="md" />
                    </Box>
                  </Flex>
                </Box>

                {/* 하단 탭바 */}
                <Flex
                  justify="space-around"
                  bg="white"
                  py={2}
                  position="fixed"
                  bottom={0}
                  w="100%"
                >
                  <IconButton
                    icon={<Icon as={FaShoppingCart} />}
                    aria-label="Home"
                    variant="ghost"
                  />
                  <IconButton
                    icon={<SearchIcon />}
                    aria-label="Search"
                    variant="ghost"
                  />
                  <IconButton
                    icon={<BellIcon />}
                    aria-label="Notifications"
                    variant="ghost"
                  />
                </Flex>
              </Box>
              <Box className="container" marginX="auto" padding={4}>
                <AdBanner />
                <ProductList
                  data={recommendations.data}
                  count={recommendations.count}
                />
              </Box>
              <p>${recommendations.toString()}</p>
            </Box>
          </Container>
        )
      )}
    </>
  )
}

export default Dashboard
