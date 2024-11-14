import {
  Container,
  Flex,
  Heading,
  Spinner,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from '@chakra-ui/react'
import { createFileRoute } from '@tanstack/react-router'
import { useQuery } from 'react-query'
import { useEffect } from 'react'
import ReactGA from 'react-ga4'

import { ApiError, ItemsService } from '../../client'
import ActionsMenu from '../../components/Common/ActionsMenu'
import Navbar from '../../components/Common/Navbar'
import useCustomToast from '../../hooks/useCustomToast'

// 구글 애널리틱스 초기화
const initializeGA = () => {
  const trackingId = import.meta.env.VITE_GA_TRACKING_ID || 'GTM-57XR9LKP';
  console.log(`Initializing Google Analytics with Tracking ID: ${trackingId}`);
  ReactGA.initialize(trackingId);
};

// 페이지뷰 추적
const trackPageView = () => {
  console.log('Tracking page view:', window.location.pathname + window.location.search);
  ReactGA.send({ hitType: 'pageview', page: window.location.pathname + window.location.search });
};

export const Route = createFileRoute('/_layout/items')({
  component: Items,
})

function Items() {
  const showToast = useCustomToast()
  const {
    data: items,
    isLoading,
    isError,
    error,
  } = useQuery('items', () => ItemsService.readItems({}))

  useEffect(() => {
    // 구글 애널리틱스 초기화 및 페이지뷰 추적
    initializeGA();
    trackPageView();
  }, [])

  if (isError) {
    const errDetail = (error as ApiError).body?.detail
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
        items && (
          <Container maxW="full">
            <Heading
              size="lg"
              textAlign={{ base: 'center', md: 'left' }}
              pt={12}
            >
              Items Management
            </Heading>
            <Navbar type={'Item'} />
            <TableContainer>
              <Table size={{ base: 'sm', md: 'md' }}>
                <Thead>
                  <Tr>
                    <Th>ID</Th>
                    <Th>Title</Th>
                    <Th>Description</Th>
                    <Th>Actions</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {items.data.map((item) => (
                    <Tr key={item.id}>
                      <Td>{item.id}</Td>
                      <Td>{item.title}</Td>
                      <Td color={!item.description ? 'gray.400' : 'inherit'}>
                        {item.description || 'N/A'}
                      </Td>
                      <Td>
                        <ActionsMenu type={'Item'} value={item} />
                      </Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            </TableContainer>
          </Container>
        )
      )}
    </>
  )
}

export default Items
