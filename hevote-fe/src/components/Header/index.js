import { useState, Fragment } from "react";
import { useNavigate } from "react-router";
import { Row, Col, Drawer } from "antd";
import { CSSTransition } from "react-transition-group";

import * as S from "./styles";


const Header = () => {
  const [isNavVisible] = useState(false);
  const [isSmallScreen] = useState(false);
  const [visible, setVisibility] = useState(false);
  const history = useNavigate();

  const showDrawer = () => {
    setVisibility(!visible);
  };

  const onClose = () => {
    setVisibility(!visible);
  };

  const MenuItem = () => {
    const redirectTo = (path) => {
      history.push(path);
    };

    return (
      <Fragment>
        <Row>
          <Col>
            <S.CustomNavLinkSmall onClick={() => redirectTo("/cast")}>
              <S.Span>Cast</S.Span>
            </S.CustomNavLinkSmall>
            <S.CustomNavLinkSmall onClick={() => redirectTo("/tally")}>
              <S.Span>Tally</S.Span>
            </S.CustomNavLinkSmall>
          </Col>
        </Row>
      </Fragment>
    );
  };

  return (
    <S.Header>
      <S.Container>
        <Row type="flex" justify="space-between" gutter={20} id="header">
          <S.LogoContainer to="/" aria-label="homepage">
            LOGO
          </S.LogoContainer>
          <S.NotHidden>
            <MenuItem />
          </S.NotHidden>
          <S.Burger onClick={showDrawer}>
            <S.Outline />
          </S.Burger>
        </Row>
        <CSSTransition
          in={!isSmallScreen || isNavVisible}
          timeout={350}
          classNames="NavAnimation"
          unmountOnExit
        >
          <Drawer closable={false} visible={visible} onClose={onClose}>
            <Col style={{ marginBottom: "2.5rem" }}>
              <S.Label onClick={onClose}>
                <Col span={12}>
                  <S.Menu>Menu</S.Menu>
                </Col>
                <Col span={12}>
                  <S.Outline padding="true" />
                </Col>
              </S.Label>
            </Col>
            <MenuItem />
          </Drawer>
        </CSSTransition>
      </S.Container>
    </S.Header>
  );
};

export default Header;
